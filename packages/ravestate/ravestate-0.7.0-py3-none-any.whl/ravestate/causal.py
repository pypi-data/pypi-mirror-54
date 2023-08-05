# Ravestate class which encapsulates a graph of signal parent/offspring instances

from typing import Set, Dict, Optional, List, Generator
from ravestate.iactivation import IActivation, ISpike, ICausalGroup
from threading import RLock
from collections import defaultdict

from reggol import get_logger
logger = get_logger(__name__)


class CausalGroup(ICausalGroup):
    """
    Class which represents a causal group graph of spike parent/offspring
     spikes (a "superspike"). These must synchronize wrt/ their (un)written
     properties and state activation candidates, such that they don't cause output races.

    Note: Always use a `with ...` construct to interact with a causal group.
     Otherwise, undefined behavior may occur due to race conditions.
    """

    # Lock for the whole causal group
    _lock: RLock
    # Remember the locked lock, since the lock member might be re-targeted in merge()
    _locked_lock: Optional[RLock]

    # Set of property names for which no writing state has been
    #  activated yet within this causal group.
    #
    # This is different from _ref_index:
    #
    #  -> _unwritten_props might lack properties that are only
    #   *temporarily* unavailable, because a writing state is still running,
    #   and might still resign, which would make that state's write prop's
    #   available again.
    #
    #  -> In this case it is useful to still see the other
    #   state activation candidates for those props in _ref_index.
    #
    # Also, _ref_index needs to be as
    #  sparse as possible to optimise performance.
    #
    _available_resources: Set[str]

    # Refcount per state activations per spike per property name.
    #  Refcount, because one activation may hold multiple references to one spike for multiple
    #  differently timed constraints. We essentially keep a {(propname, spike, activation, refcount)}
    #  index structure, that will be necessary for the following use-cases:
    #
    #  * Determining whether an activation is the most specific for a certain property set
    #    -> Gather state activations per spike (i) per property (p), sort by specificity
    #    -> O(i * log p)
    #  * Determining whether a spike is stale (no more activation references)
    #    -> For every property name (p), check whether the spike (i) is registered
    #    -> O(p * log i)
    #
    #  Container operations:
    #
    #  * Inserting a spike (i) / state activation (a)
    #    -> O(log p + log i + log a)
    #  * Removing a state activation (a) for a spike (i) (for each of the state's referenced properties (p))
    #    -> O(log p + log i + log a)
    #  * Wiping a spike (i)
    #    -> O(p * log i)
    #
    _ref_index: Dict[
        str,  # Resource name
        Dict[
            ISpike,
            Dict[
                IActivation,
                int
            ]
        ]
    ]

    # Detached signal references need to be tracked separately.
    #  The reason is, that the activations with detached signal
    #  constraints do not expect to need any consent for their
    #  write-activities from those signal's causal groups.
    # They are therefore not de-referenced upon consumed(), but upon wiped()
    #  or rejected().
    _detached_ref_index: Dict[
        ISpike,
        Dict[
            IActivation,
            int
        ]
    ]

    # Dictionary, which records activations that may cause particular signal spikes
    #  by consuming spikes from this causal group. Whenever an activation acquires or dereferences
    #  a spike from this causal group, or notify_spike(signal) is called, the dictionary is updated to
    #  add/remove activations. A special case occurs, when an activation finishes
    #  without causing some of it's possible effects (spikes): Then, effect_not_caused(effects) will
    #  be called by the activation with the forgone signals: If for any of the forgone signal spikes
    #  there are no other registered activations which could cause the same spikes,
    #  Activation.effect_not_caused(effects, causal_group) will be called on all activations registered
    #  in this causal group.
    _uncaused_spikes: Dict[
        str,
        Dict[
            IActivation,
            int
        ]
    ]

    # Names of member spikes for __repr__, added by Spike ctor
    signal_names: List[str]

    # Object to count the number of CausalGroups merged in this instance
    merges: List[int]

    def __init__(self, resources: Set[str]):
        """
        Create a new causal group, with a set of unwritten props.
        """
        self.signal_names = []
        self.merges = [1]
        self._lock = RLock()
        self._locked_lock = None
        self._available_resources = resources.copy()
        self._ref_index = {
            # TODO: Create refcount prop entries on demand
            prop: defaultdict(lambda: defaultdict(int))
            for prop in resources
        }
        self._detached_ref_index = defaultdict(lambda: defaultdict(int))
        self._uncaused_spikes = defaultdict(lambda: defaultdict(int))

    def __del__(self):
        with self._lock:
            self.merges[0] -= 1
        logger.debug(f"Deleted {self}")

    def __enter__(self) -> 'CausalGroup':
        # Remember current lock, since it might change,
        # if the lock object is switched in merge()
        lock = self._lock
        lock.acquire()
        if lock != self._lock:
            lock.release()
            return self.__enter__()
        # Remember the locked lock, since the lock member might be re-targeted in merge()
        self._locked_lock = self._lock
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        assert self._locked_lock
        self._locked_lock.release()
        if self._locked_lock.acquire(False):
            # Test whether lock is still owned (recursively).
            self._locked_lock.release()
        else:
            # If the lock is not owned anymore, it isn't locked by this thread anymore
            #  -> acquire would block, returns False.
            self._locked_lock = None

    def __eq__(self, other) -> bool:
        return isinstance(other, CausalGroup) and other._lock == self._lock

    def __hash__(self):
        return self._lock.__hash__()

    def __repr__(self):
        if len(self.signal_names) < 4:
            spikes = ','.join(self.signal_names)
        else:
            spikes = f"{self.signal_names[0]},...[{len(self.signal_names)-2} more],{self.signal_names[-1]}"
        return f"CausalGroup*{self.merges[0]}@{hex(id(self._lock))[2:]}({spikes})"

    def merge(self, other: 'CausalGroup'):
        """
        Merge this causal group with another. Unwritten props will become
         the set intersection of this group's unwritten props and
         other's unwritten props. consumed() will be called with
         all properties that are consumed by other, but not this.
        Afterwards, other's member objects will be set to this's.
        """
        logger.debug(f"=======> CausalGroup.merge({self} | {other})")

        # Intersect _available_resources
        self._available_resources = self._available_resources & other._available_resources

        # Intersect/merge _ref_index
        allowed_propnames = self._ref_index.keys() & other._ref_index.keys()
        self.consumed(set(self._ref_index.keys()) - allowed_propnames)
        other.consumed(set(other._ref_index.keys()) - allowed_propnames)
        for prop, spikes in other._ref_index.items():
            for spike, act_refcount in spikes.items():
                for act, refcount in act_refcount.items():
                    if refcount > 0:
                        self._ref_index[prop][spike][act] += refcount

        # Merge _detached_ref_index
        self._detached_ref_index.update(other._detached_ref_index)

        # Merge _activations_per_effect
        for signal, refc_per_act in other._uncaused_spikes.items():
            my_refc_per_act = self._uncaused_spikes[signal]
            for act, refc in refc_per_act.items():
                my_refc_per_act[act] += refc

        # Merge signal names/merge count
        self.signal_names += other.signal_names
        self.merges[0] += other.merges[0]

        # Retarget other's members
        other.signal_names = self.signal_names
        other.merges = self.merges
        other._lock = self._lock
        other._available_resources = self._available_resources
        other._ref_index = self._ref_index
        other._detached_ref_index = self._detached_ref_index

    def acquired(self, spike: 'ISpike', acquired_by: IActivation, detached: bool) -> bool:
        """
        Called by Activation to notify the causal group, that
         it is being referenced by an activation constraint for a certain member spike.

        * `spike`: State activation instance, which is now being
         referenced by the specified causal group.

        * `acquired_by`: State activation instance,
         which is interested in this property.

        * `detached`: Tells the causal group, whether the reference is detached,
          and should therefore receive special treatment.

        **Returns:** Returns True if all of the acquiring's write-props are
         free, and the group now refs. the activation, False otherwise.
        """
        # Make sure that all properties are actually still writable
        if detached:
            self._detached_ref_index[spike][acquired_by] += 1
        else:
            for prop in acquired_by.resources():
                if prop not in self._ref_index:
                    return False
            for prop in acquired_by.resources():
                self._ref_index[prop][spike][acquired_by] += 1
            self._change_effect_causes(acquired_by, 1)

        logger.debug(f"{self}.acquired({spike} by {acquired_by})")
        return True

    def rejected(self, spike: 'ISpike', rejected_by: IActivation, reason: int) -> None:
        """
        Called by a state activation, to notify the group that a member spike
         is no longer being referenced for the given state's write props.
        This may be because ... <br>
        ... the activation's dereference function was called. (reason=0) <br>
        ... the spike got too old. (reason=1) <br>
        ... the activation happened and is dereferencing it's spikes. (reason=2)

        * `spike`: The member spike whose ref-set should be reduced.

        * `rejected_by`: State activation instance, which is no longer
         interested in this property.

        * `reason`: See about.
        """
        def _decrement_refcount(refcount_for_act_for_spike):
            if spike in refcount_for_act_for_spike and rejected_by in refcount_for_act_for_spike[spike]:
                remaining_refcount = refcount_for_act_for_spike[spike][rejected_by]
                if remaining_refcount > 0:
                    refcount_for_act_for_spike[spike][rejected_by] -= 1
                    if remaining_refcount > 1:
                        # do not fall through to ref deletion
                        return
                else:
                    logger.error(f"Attempt to deref group for unref'd activation {rejected_by.name}")
                del refcount_for_act_for_spike[spike][rejected_by]

        _decrement_refcount(self._detached_ref_index)
        for prop in rejected_by.resources():
            if prop in self._ref_index:
                _decrement_refcount(self._ref_index[prop])
                if len(self._ref_index[prop][spike]) == 0:
                    del self._ref_index[prop][spike]

        self._change_effect_causes(rejected_by, -1)

        logger.debug(f"{self}.rejected({spike} by {rejected_by})")

    def consent(self, ready_suitor: IActivation) -> bool:
        """
        Called by constraint, to inquire whether this causal group would happily
         be consumed for the given state activation's properties.
        This will be called periodically on the group by state activations
         that are ready to go. Therefore, a False return value from this
         function is never a final judgement (more like a "maybe later").

        * `ready_suitor`: The state activation which would like to consume
         this instance for it's write props.

        **Returns:** True if this instance agrees to proceeding with the given consumer
         for the consumer's write props, False otherwise.
        """
        specificity = ready_suitor.specificity()
        higher_specificity_acts = set()
        highest_higher_specificity = .0
        highest_higher_specificity_act = None

        # Go through the ready_suitors write-props. For each property,
        #  check whether it is still available, and also check whether
        #  there are other activations for this property that have higher specificity.
        for prop in ready_suitor.resources():
            if prop in self._available_resources:
                for spike in self._ref_index[prop]:
                    for candidate in self._ref_index[prop][spike]:
                        if candidate not in higher_specificity_acts:
                            cand_specificity = candidate.specificity()
                            if cand_specificity > specificity:
                                higher_specificity_acts.add(candidate)
                                if cand_specificity > highest_higher_specificity:
                                    highest_higher_specificity = cand_specificity
                                    highest_higher_specificity_act = candidate
            else:
                # Easy exit condition: prop not free for writing
                logger.debug(f"{self}.consent({ready_suitor})->N: {prop} unavailable.")
                return False

        if higher_specificity_acts:
            for act in higher_specificity_acts:
                act.pressure(self)
            logger.debug(
                f"{self}.consent({ready_suitor})->N: "
                f"{str(specificity)[:4]} < {str(highest_higher_specificity)[:4]} "
                f"({highest_higher_specificity_act} + {len(higher_specificity_acts)-1} others)")
            return False

        logger.debug(f"{self}.consent({ready_suitor})->Y")
        return True

    def activated(self, act: IActivation):
        """
        Called by activation which previously received a go-ahead
         from consent(), when it is truly proceeding with
         running (after it got the go-ahead from all it's depended=on
         causal groups).

        * `act`: The activation that is now running.
        """
        # Mark the consented w-props as unavailable
        self._available_resources -= act.resources()

    def resigned(self, act: IActivation) -> None:
        """
        Called by activation, to let the causal group know that it failed,
         and a less specific activation may now be considered for
         the resigned state's write props.

        * `act`: The activation that is unexpectedly not consuming it's resources,
         because it's state resigned/failed.
        """
        # Mark the act's w-props as available again
        self._available_resources |= act.resources()

    def consumed(self, resources: Set[str]) -> None:
        """
        Called by activation to notify the group, that it has been
         consumed for the given set of properties.

        * `resources`: The properties which have been consumed.
        """
        if not resources:
            return
        acts_to_forget = set()
        for resource in resources.copy():
            # Notify all concerned activations, that the
            # spikes they are referencing are no longer available
            for spike in self._ref_index[resource].copy():
                for act in self._ref_index[resource][spike].copy():
                    act.dereference(spike=spike, reacquire=True, reject=True)
                    acts_to_forget.add(act)
            del self._ref_index[resource]
        for act in acts_to_forget:
            self._change_effect_causes(act, None)
        logger.debug(f"{self}.consumed({resources})")

    def wiped(self, spike: 'ISpike') -> None:
        """
        Called by a spike, to notify the causal group that
         the instance was wiped and should no longer be remembered.

        * `spike`: The instance that should be henceforth forgotten.
        """
        def _remove_spike_from_index(refcount_for_act_for_spike):
            if spike in refcount_for_act_for_spike:
                for act in refcount_for_act_for_spike[spike]:
                    act.dereference(spike=spike, reacquire=True)
                del refcount_for_act_for_spike[spike]
        for prop in self._ref_index:
            _remove_spike_from_index(self._ref_index[prop])
        _remove_spike_from_index(self._detached_ref_index)

    def stale(self, spike: 'ISpike') -> bool:
        """
        Determine, whether a spike is stale (has no
        remaining interested activations and no children).

        **Returns:** True, if no activations reference the given
         spike for any unwritten property. False otherwise.
        """
        for prop in self._ref_index:
            if spike in self._ref_index[prop]:
                if len(self._ref_index[prop][spike]) > 0:
                    return False
                else:
                    # Do some cleanup
                    del self._ref_index[prop][spike]
        if spike in self._detached_ref_index:
            if len(self._detached_ref_index[spike]) > 0:
                return False
            else:
                # Do some cleanup
                del self._detached_ref_index[spike]
        result = not spike.has_offspring()
        return result

    def notify_spike(self, sig: str):
        self.signal_names.append(sig)
        if sig in self._uncaused_spikes:
            del self._uncaused_spikes[sig]

    def _change_effect_causes(self, act: IActivation, change: Optional[int]):
        for sig in act.possible_signals():
            sig_present_or_change_positive = sig in self._uncaused_spikes or (change is not None and change > 0)
            if sig_present_or_change_positive:
                if (change is None or change < 0) and act not in self._uncaused_spikes[sig]:
                    continue
                if change is None:
                    del self._uncaused_spikes[sig][act]
                else:
                    self._uncaused_spikes[sig][act] += change
                    if self._uncaused_spikes[sig][act] <= 0:
                        del self._uncaused_spikes[sig][act]
                if len(self._uncaused_spikes[sig]) == 0:
                    for act_to_notify in set(self._non_detached_activations()):
                        act_to_notify.effect_not_caused(self, sig.id())
                    del self._uncaused_spikes[sig]

    def _non_detached_activations(self) -> Generator[IActivation, None, None]:
        yielded_activations = set()
        for refc_per_act_per_spike in self._ref_index.values():
            for refc_per_act in refc_per_act_per_spike.values():
                for act in refc_per_act:
                    if act not in yielded_activations:
                        yielded_activations.add(act)
                        yield act

    def check_reference_sanity(self) -> bool:
        """
        Make sure, that the refcount-per-act-per-spike-per-resource value sum
         is equal to the number of spikes from this causal group acquired per activation
         for each activation in the index.
        :return: True if the criterion is fulfilled, False otherwise.
        """
        result = True
        signals_with_cause = set()
        for act in self._non_detached_activations():
            sum_refcount = sum(
                refc_per_act[act]
                for resource in act.resources()
                for refc_per_act in self._ref_index[resource].values() if act in refc_per_act)
            sum_spikes = sum(
                len(act.resources())
                for signal in act.constraint.signals() if signal.spike and signal.spike.causal_group() == self)
            if sum_spikes != sum_refcount:
                logger.error(f"Mutual refcount mismatch: {self} -> {sum_refcount} : {sum_spikes} <- {act}")
                result = False
            for sig in act.possible_signals():
                signals_with_cause.add(sig)
                if sig in self._uncaused_spikes:
                    causes = sum_spikes / len(act.resources())
                    if self._uncaused_spikes[sig][act] != causes:
                        logger.error(f"Signal cause mismatch for {sig} by {act}: is {self._uncaused_spikes[sig][act]}, "
                                     f"should be {causes}")
                        result = False
        for signal in set(self._uncaused_spikes.keys())-signals_with_cause:
            logger.error(f"Signal cause mismatch for {signal}: is {self._uncaused_spikes[signal]}, "
                         f"should be ZERO")
            result = False
        return result
