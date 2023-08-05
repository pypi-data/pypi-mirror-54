import os
import multiprocessing as mp
import random
from multiprocessing.connection import Connection
import time
from typing import Set, Dict, Optional, Tuple
from tempfile import mkstemp
import requests

import ravestate as rs

from telegram import Bot, Update, TelegramError, ChatAction
from telegram.ext import Updater, MessageHandler, Filters, Dispatcher

from scientio.ontology.node import Node
from scientio.session import Session
from scientio.ontology.ontology import Ontology

from reggol import get_logger
logger = get_logger(__name__)

import ravestate_rawio as rawio
import ravestate_interloc as interloc
import ravestate_ontology as ontology
import ravestate_emotion as emotion
import ravestate_verbaliser as verbaliser


MODULE_NAME: str = 'telegramio'
TOKEN_CONFIG_KEY: str = "telegram-token"
CHILD_CONN_CONFIG_KEY: str = "child_conn"
CHILD_FILES_CONFIG_KEY: str = "child_config_files"
ALL_IN_ONE_CONTEXT_CONFIG_KEY: str = 'all_in_one_context'
CHAT_LIFETIME: str = 'chat_lifetime'


class Timestamp:
    value: float

    def __init__(self):
        self.value = time.time()

    def update(self):
        self.value = time.time()

    def age(self):
        return time.time() - self.value


# active_chats contains all active "Chats".
# Maps chat_id to a tuple consisting of the timestamp of the last message in this chat and a Pipe.
# If all chats run in one process, the pipe-field is set to None
active_chats: Dict[int, Tuple[Timestamp, Optional[mp.connection.Connection]]] = dict()
# active_users contains user_ids of all Users that currently engage with the bot.
# At the same time a User can talk to the bot in personal and group chats but only is in active_users once.
# A user_id is mapped to a set containing the chat_id of every Chat that the User is involved in
active_users: Dict[int, Set[int]] = dict()

SHY_EMOJIS = ["\U0000263A"]
SURPRISE_EMOJIS = ["\U0001F914"]
HAPPY_EMOJIS = ["\U0001F60A", "\U0001F603"]
AFFECTIONATE_EMOJIS = ["\U0001F618", "\U0001F970"]


@rs.state(cond=rs.sig_startup)
def telegram_run(ctx: rs.ContextWrapper):
    """
    Starts up the telegram bot and adds a handler to write incoming messages to rawio:in
    """

    @rs.receptor(ctx_wrap=ctx, write=rawio.prop_in)
    def text_receptor(ctx: rs.ContextWrapper, message_text: str):
        """
        Writes the message_text to rawio:in
        """
        ctx[rawio.prop_in] = message_text

    @rs.receptor(ctx_wrap=ctx, write=rawio.prop_pic_in)
    def photo_receptor(ctx: rs.ContextWrapper, photo_path):
        """
        Handles photo messages, write to rawio:pic_in
        """
        ctx[rawio.prop_pic_in] = photo_path

    @rs.receptor(ctx_wrap=ctx, write=interloc.prop_all)
    def push_telegram_interloc(ctx: rs.ContextWrapper, telegram_node: Node, name: str):
        """
        Push the telegram_node into interloc:all:name
        """
        if ctx.push(parent_property_or_path=interloc.prop_all, child=rs.Property(name=name, default_value=telegram_node)):
            logger.debug(f"Pushed {telegram_node} to interloc:all")

    def make_sure_effective_user_exists(update: Update):
        """
        Retrieves scientio Node of User if it exists, otherwise creates it in the scientio session
        Calls the push_telegram_interloc receptor to push the scientio node into interloc:all
        Adds the User to the set of active_users and the chat to the set of active_chats
        """
        active_chats[update.effective_chat.id] = (Timestamp(), None)
        if update.effective_user.id in active_users:
            active_users[update.effective_user.id].add(update.effective_chat.id)
        else:
            # set up scientio
            if ontology.initialized.wait():
                sess: Session = ontology.get_session()
                onto: Ontology = ontology.get_ontology()

                # create scientio Node of type TelegramPerson
                query = Node(metatype=onto.get_type("TelegramPerson"))
                prop_dict = {'telegram_id': update.effective_user.id}
                if update.effective_user.username:
                    prop_dict['name'] = update.effective_user.username
                if update.effective_user.full_name:
                    prop_dict['full_name'] = update.effective_user.full_name
                query.set_properties(prop_dict)

                node_list = sess.retrieve(query)
                if not node_list:
                    telegram_node = sess.create(query)
                    logger.info(f"Created new Node in scientio session: {telegram_node}")
                elif len(node_list) == 1:
                    telegram_node = node_list[0]
                else:
                    logger.error(f'Found multiple TelegramPersons that matched query: {update.message.chat_id} '
                                 f'in scientio session. Cannot push node to interloc:all!')
                    return

                # push chat-Node
                push_telegram_interloc(telegram_node, update.effective_chat.id)
                active_users[update.effective_user.id] = {update.effective_chat.id}

    def handle_text(bot: Bot, update: Update):
        """
        Handle incoming text messages
        """
        make_sure_effective_user_exists(update)
        text_receptor(update.effective_message.text)

    def handle_photo(bot: Bot, update: Update):
        """
        Handle incoming photo messages.
        """
        make_sure_effective_user_exists(update)
        photo_index = 2  # Seems like a good size index. TODO: Make configurable
        while photo_index >= len(update.effective_message.photo):
            photo_index -= 1
            if photo_index < 0:
                logger.error("Telegram photo handler was called, but no photo received!")
                return
        file_descr = bot.get_file(update.effective_message.photo[photo_index].file_id)
        photo = requests.get(file_descr.file_path)
        file_path = mkstemp()[1]
        with open(file_path, 'wb') as file:
            file.write(photo.content)
        photo_receptor(file_path)

    def handle_input_multiprocess(bot: Bot, update: Update):
        """
        Handle incoming messages
        """
        if update.effective_chat.id not in active_chats:
            add_new_child_process(update.effective_chat.id)
        # write (bot, update) to Pipe
        active_chats[update.effective_chat.id][0].update()
        logger.info(f"INPUT: {update.effective_message.text}")
        active_chats[update.effective_chat.id][1].send((bot, update))
        # send typing symbol
        bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    def add_new_child_process(chat_id):
        """
        Adds the chat of the incoming message to the set of active_chats
        Creates new Ravestate Context in new Process for the new chat and
        sets up a bidirectional Pipe for communication between Master and Child Processes
        """
        # start method has to be 'spawn'
        mp_context = mp.get_context('spawn')
        # Pipe to communicate between Master Process and all children
        parent_conn, child_conn = mp.Pipe()
        # create commandline args for child config file
        args = []
        child_config_paths_list = ctx.conf(key=CHILD_FILES_CONFIG_KEY)
        for child_config_path in child_config_paths_list:
            args += ['-f', child_config_path]
        # set up new Process and override child_conn with the Pipe-Connection
        p = mp_context.Process(target=rs.create_and_run_context,
                               args=(*args,),
                               kwargs={'runtime_overrides': [(MODULE_NAME, CHILD_CONN_CONFIG_KEY, child_conn)]})
        p.start()
        active_chats[chat_id] = (Timestamp(), parent_conn)

    def error(bot: Bot, update: Update, error: TelegramError):
        """
        Log Errors caused by Updates.
        """
        logger.warning(f'Update {update.effective_message} caused error {error.message}')

    def _manage_children(updater):
        """
        Receive messages from children via Pipe and then send them to corresponding Telegram Chat.
        Remove chats when they get older than the chat lifetime.
        :param updater: The Updater of the telegram-Bot
        """
        chat_lifetime = ctx.conf(key=CHAT_LIFETIME) * 60  # conversion from minutes to seconds
        while not ctx.shutting_down():
            removable_chats = set()
            removable_users = set()
            # wait for children to write to Pipe and then send message to chat
            tick_interval = 1. / ctx.conf(mod=rs.CORE_MODULE_NAME, key=rs.TICK_RATE_CONFIG_KEY)
            time.sleep(tick_interval)
            for chat_id, (last_msg_timestamp, parent_pipe) in active_chats.items():
                if parent_pipe.poll():
                    try:
                        msg = parent_pipe.recv()
                        if isinstance(msg, str):
                            logger.info(f"OUTPUT: {msg}")
                            updater.bot.send_message(chat_id=chat_id, text=msg)
                        else:
                            logger.error(f'Tried sending non-str object as telegram message: {str(msg)}')
                    except EOFError:
                        # Child pipe was closed
                        parent_pipe.close()
                        removable_chats.add(chat_id)
                        continue
                # remove chat from active_chats if inactive for too long
                if last_msg_timestamp.age() > chat_lifetime:
                    parent_pipe.close()
                    removable_chats.add(chat_id)

            for chat_id in removable_chats:
                active_chats.pop(chat_id)
                for user_id, chat_ids in active_users.items():
                    # remove chat from chats that the user is part of
                    chat_ids.discard(chat_id)
                    if len(chat_ids) == 0:
                        # user is no longer part of any active chats
                        removable_users.add(user_id)
            for user_id in removable_users:
                active_users.pop(user_id)

    def _bootstrap_telegram_master():
        """
        Handle TelegramIO as the Master Process.
        Start the bot, and handle incoming telegram messages.
        """
        token = ctx.conf(key=TOKEN_CONFIG_KEY)
        if not token:
            logger.error(f'{TOKEN_CONFIG_KEY} is not set. Shutting down telegramio')
            return rs.Delete()
        child_config_paths_list = ctx.conf(key=CHILD_FILES_CONFIG_KEY)
        if not ctx.conf(key=ALL_IN_ONE_CONTEXT_CONFIG_KEY) and (
                not child_config_paths_list or not isinstance(child_config_paths_list, list)
                or not all(os.path.isfile(child_config_path) for child_config_path in child_config_paths_list)):
            logger.error(f'{CHILD_FILES_CONFIG_KEY} is not set (correctly). Shutting down telegramio')
            return rs.Delete()

        updater: Updater = Updater(token)
        # Get the dispatcher to register handlers
        dispatcher: Dispatcher = updater.dispatcher
        if ctx.conf(key=ALL_IN_ONE_CONTEXT_CONFIG_KEY):
            # handle noncommand-messages with the matching handler
            dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
            dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
        else:
            dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, handle_input_multiprocess))
        # log all errors
        dispatcher.add_error_handler(error)
        # Start the Bot
        updater.start_polling()  # non blocking

        if not ctx.conf(key=ALL_IN_ONE_CONTEXT_CONFIG_KEY):
            _manage_children(updater)

    def _bootstrap_telegram_child():
        """
        Handle TelegramIO as a Child Process.
        Listen to Pipe and handle incoming texts and photos.
        """
        try:
            while not ctx.shutting_down():
                # receive Bot,Update for telegram chat
                bot, update = child_conn.recv()  # blocking
                if update.effective_message.photo:
                    handle_photo(bot, update)
                elif update.effective_message.text:
                    if update.effective_message.text.strip().lower() in verbaliser.get_phrase_list("farewells"):
                        send_on_telegram(ctx, verbaliser.get_random_phrase("farewells"))
                        logger.info("Shutting down child process")
                        ctx.shutdown()
                    handle_text(bot, update)
                else:
                    logger.error(f"{MODULE_NAME} received an update it cannot handle.")
        except EOFError:
            # Pipe was closed -> Parent was killed or parent has closed the pipe
            logger.info("Pipe was closed, therefore the telegram-child will shut down.")
            ctx.shutdown()

    child_conn = ctx.conf(key=CHILD_CONN_CONFIG_KEY)
    is_master_process = child_conn is None
    if is_master_process:
        return _bootstrap_telegram_master()
    else:
        _bootstrap_telegram_child()


def send_on_telegram(ctx: rs.ContextWrapper, text: str):
    """
    If all telegram chats should be in the same context, sends the text to every currently active chat.
    Otherwise it only sends output using the Pipe if it is a child process
    """
    if not text or not isinstance(text, str):
        return rs.Resign()

    if ctx.conf(key=ALL_IN_ONE_CONTEXT_CONFIG_KEY):
        # TODO don't instantiate the updater every time
        token = ctx.conf(key=TOKEN_CONFIG_KEY)
        if not token:
            logger.error('telegram-token is not set. Shutting down telegramio')
            return rs.Delete()
        updater: Updater = Updater(token)
        for chat_id in active_chats.keys():
            updater.bot.send_message(chat_id=chat_id, text=text)
    else:
        child_conn = ctx.conf(key=CHILD_CONN_CONFIG_KEY)
        if child_conn:
            # Child Process -> write to Pipe
            child_conn.send(text)
        else:
            # Master Process -> State not needed
            return rs.Delete()


@rs.state(read=rawio.prop_out)
def telegram_output(ctx: rs.ContextWrapper):
    """
    Sends the content of rawio:out on telegram
    """
    text = ctx[rawio.prop_out.changed()]
    return send_on_telegram(ctx=ctx, text=text.lower().strip())


@rs.state(cond=emotion.sig_shy)
def show_shy(ctx: rs.ContextWrapper):
    logger.info("Sending shy emoji on telegram")
    send_on_telegram(ctx=ctx, text=random.choice(SHY_EMOJIS))


@rs.state(cond=emotion.sig_surprise)
def show_surprise(ctx: rs.ContextWrapper):
    logger.info("Sending surprise emoji on telegram")
    send_on_telegram(ctx=ctx, text=random.choice(SURPRISE_EMOJIS))


@rs.state(cond=emotion.sig_happy)
def show_happy(ctx: rs.ContextWrapper):
    logger.info("Sending happy emoji on telegram")
    send_on_telegram(ctx=ctx, text=random.choice(HAPPY_EMOJIS))


@rs.state(cond=emotion.sig_affectionate)
def show_affectionate(ctx: rs.ContextWrapper):
    logger.info("Sending affectionate emoji on telegram")
    send_on_telegram(ctx=ctx, text=random.choice(AFFECTIONATE_EMOJIS))
