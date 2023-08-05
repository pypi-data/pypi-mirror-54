import time
from typing import Dict

import ravestate as rs

from reggol import get_logger
logger = get_logger(__name__)


ROS2_AVAILABLE = True
try:
    import rclpy
except ImportError:
    logger.error("Could not import rclpy. Please make sure to have ROS2 installed.")
    ROS2_AVAILABLE = False

NODE_NAME_CONFIG_KEY = "ros2-node-name"
SPIN_FREQUENCY_CONFIG_KEY = "ros2-spin-frequency"

global_prop_set = set()
global_node = None


def set_node_once(ros2_node):
    """
    May be called once to override the internal ros2 node, which will
     be created otherwise. ravestate_ros2 only supports one internal
     node for compatibility with ROS1<->ROS2 bridge.
    :param ros2_node: The node which should be adapted and spun by ravestate_ros2.
    """
    global global_node
    if global_node:
        logger.error("Attempt to call set_node_once twice, or after context.run().")
    else:
        global_node = ros2_node


@rs.state(cond=rs.sig_startup)
def sync_ros_properties(ctx: rs.ContextWrapper):
    """
    State that creates a ROS2-Node, registers all Ros2SubProperties and Ros2PubProperties in ROS2 and keeps them synced
    """
    global global_prop_set, global_node

    # check for ROS2 availability
    if not ROS2_AVAILABLE:
        logger.error("ROS2 is not available, therefore all ROS2-Properties "
                     "will be just normal properties without connection to ROS2!")
        return rs.Delete()

    # get config stuff
    node_name = ctx.conf(key=NODE_NAME_CONFIG_KEY)
    if not node_name:
        logger.error(f"{NODE_NAME_CONFIG_KEY} is not set. Shutting down ravestate_ros2")
        return rs.Delete()
    spin_frequency = ctx.conf(key=SPIN_FREQUENCY_CONFIG_KEY)
    if spin_frequency is None or spin_frequency < 0:
        logger.error(f"{SPIN_FREQUENCY_CONFIG_KEY} is not set or less than 0. Shutting down ravestate_ros2")
        return rs.Delete()
    if spin_frequency == 0:
        spin_sleep_time = 0
    else:
        spin_sleep_time = 1 / spin_frequency

    # init ROS
    if not rclpy.ok():
        rclpy.init()
    if not global_node:
        global_node = rclpy.create_node(node_name)

    global global_prop_set
    # current_props: hash -> subscription/publisher
    current_props: Dict = dict()

    # ROS-Context Sync Loop
    while not ctx.shutting_down():
        # remove deleted props
        removed_props = current_props.keys() - global_prop_set
        for prop_hash in removed_props:
            item = current_props[prop_hash]
            if isinstance(item, rclpy.subscription.Subscription):
                global_node.destroy_subscription(item)
            elif isinstance(item, rclpy.publisher.Publisher):
                global_node.destroy_publisher(item)
            elif isinstance(item, rclpy.client.Client):
                global_node.destroy_client(item)
            current_props.pop(prop_hash)

        # add new props
        new_props = global_prop_set - current_props.keys()
        for prop in new_props:
            # register subscribers in ROS
            if isinstance(prop, Ros2SubProperty):
                # register in context
                @rs.receptor(ctx_wrap=ctx, write=prop.id())
                def ros_to_ctx_callback(ctx, msg, prop_name: str):
                    ctx[prop_name] = msg

                prop.ros_to_ctx_callback = ros_to_ctx_callback
                prop.subscription = global_node.create_subscription(prop.msg_type, prop.topic, prop.ros_subscription_callback)
                current_props[prop.__hash__()] = prop.subscription
            # register publishers in ROS
            if isinstance(prop, Ros2PubProperty):
                prop.publisher = global_node.create_publisher(prop.msg_type, prop.topic)
                current_props[prop.__hash__()] = prop.publisher
            # register clients in ROS
            if isinstance(prop, Ros2CallProperty):
                prop.client = global_node.create_client(prop.service_type, prop.service_name)
                current_props[prop.__hash__()] = prop.client

            # replace prop with hash in global_props
            global_prop_set.remove(prop)
            global_prop_set.add(prop.__hash__())

        # spin once
        rclpy.spin_once(global_node, timeout_sec=0)
        time.sleep(spin_sleep_time)

    global_node.destroy_node()
    rclpy.shutdown()


class Ros2SubProperty(rs.Property):
    def __init__(self, name: str, topic: str, msg_type, default_value=None, always_signal_changed: bool = True, boring: bool = False):
        """
        Initialize Property

        * `name`: Name of the property

        * `topic`: ROS2-Topic that should be subscribed

        * `msg_type`: ROS2-Message type of messages in the topic

        * `default_value`: Default value of the property

        * `always_signal_changed`: if signal:changed should be emitted if value is written again without changing
        """
        super().__init__(
            name=name,
            allow_read=True,
            allow_write=True,
            allow_push=False,
            allow_pop=False,
            default_value=default_value,
            always_signal_changed=always_signal_changed,
            boring=boring)
        self.topic = topic
        self.msg_type = msg_type
        self.subscription = None
        self.ros_to_ctx_callback = None
        global global_prop_set
        global_prop_set.add(self)

    def __del__(self):
        global global_prop_set
        global_prop_set.remove(self.__hash__())

    def clone(self):
        result = Ros2SubProperty(
            name=self.name,
            topic=self.topic,
            msg_type=self.msg_type,
            default_value=self.value,
            always_signal_changed=self.always_signal_changed)
        result.set_parent_path(self.parent_path)
        return result

    def ros_subscription_callback(self, msg):
        """
        Writes the message from ROS to the property

        * `msg`: ROS2-Message that should be written into the property
        """
        if self.ros_to_ctx_callback:
            logger.debug(f"{self.id()} received message {str(msg)} from topic {self.topic}")
            self.ros_to_ctx_callback(msg=msg, prop_name=self.id())


class Ros2PubProperty(rs.Property):
    def __init__(self, name: str, topic: str, msg_type, boring: bool = False):
        """
        Initialize Property

        * `name`: Name of the property

        * `topic`: ROS2-Topic that messages should be pubished to

        * `msg_type`: ROS2-Message type of messages in the topic
        """
        super().__init__(
            name=name,
            allow_read=True,
            allow_write=True,
            allow_push=False,
            allow_pop=False,
            default_value=None,
            always_signal_changed=True,
            boring=boring)
        self.topic = topic
        self.msg_type = msg_type
        self.publisher = None
        global global_prop_set
        global_prop_set.add(self)

    def __del__(self):
        global global_prop_set
        global_prop_set.remove(self.__hash__())

    def clone(self):
        result = Ros2PubProperty(
            name=self.name,
            topic=self.topic,
            msg_type=self.msg_type)
        result.set_parent_path(self.parent_path)
        return result

    def write(self, value):
        """
        Publish value on ROS

        * `value`: ROS2-Message that should be published
        """
        if super().write(value):
            if self.publisher:
                logger.debug(f"{self.id()} is publishing message {str(value)} on topic {self.topic}")
                self.publisher.publish(value)
            elif ROS2_AVAILABLE:
                logger.error(f"Message {str(value)} on topic {self.topic} "
                             f"cannot be published because publisher was not registered in ROS")


class Ros2CallProperty(rs.Property):
    def __init__(self, name: str, service_name: str, service_type, call_timeout: float = 10.0, boring: bool = False):
        """
        Initialize Property

        * `name`: Name of the property

        * `service_name`: ROS2-Service that should be called

        * `service_type`: Type of the service used

        * `call_timeout`: Timeout when waiting for availability of a service in seconds
        """
        super().__init__(
            name=name,
            allow_read=True,
            allow_write=True,
            allow_push=False,
            allow_pop=False,
            default_value=None,
            always_signal_changed=False,
            boring=boring)
        self.service_name = service_name
        self.service_type = service_type
        self.call_timeout = call_timeout
        self.client = None
        global global_prop_set
        global_prop_set.add(self)

    def __del__(self):
        global global_prop_set
        global_prop_set.remove(self.__hash__())

    def clone(self):
        result = Ros2CallProperty(
            name=self.name,
            service_name=self.service_name,
            service_type=self.service_type,
            call_timeout=self.call_timeout)
        result.set_parent_path(self.parent_path)
        return result

    def write(self, value):
        """
        Call Service and receive result directly in the property.
        Blocks during service-call.
        If service is not available, writes None into the property value and returns.

        * `value`: Either Request-Object for the service or dict containing the attributes of the Request
        """
        if super().write(value):
            if self.client:
                if not self.client.wait_for_service(timeout_sec=self.call_timeout):
                    logger.error(f'service {self.service_name} not available')
                    super().write(None)
                    return

                if isinstance(value, self.service_type.Request):
                    # value is already Request
                    req = value
                else:
                    # value is dict {"param1": value1, "param2": value2}
                    req = self.service_type.Request(**value)

                logger.debug(f"{self.id()} is sending request {str(req)} to service {self.service_name}")
                result = self.client.call(req)
                super().write(result)

            elif ROS2_AVAILABLE:
                logger.error(f"Request {str(value)} to service {self.service_name} "
                             f"cannot be sent because client was not registered in ROS")

