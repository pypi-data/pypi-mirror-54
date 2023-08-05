from ravestate.module import Module
from ravestate_telegramio import telegram_bot

import ravestate_rawio as rawio
import ravestate_interloc as interloc
import ravestate_ontology as ontology
import ravestate_emotion as emotion


CONFIG = {
    # Token for the Telegram Bot
    telegram_bot.TOKEN_CONFIG_KEY: "",
    # Not to be set in a config file or via the command line. Will be set by master process as a runtime_override.
    telegram_bot.CHILD_CONN_CONFIG_KEY: None,
    # The config-paths listed here will be used for each new telegram chat (if they don't share the same context).
    # Currently only absolute paths are supported
    telegram_bot.CHILD_FILES_CONFIG_KEY: [],
    # Whether all telegram chats should share the same context or not
    telegram_bot.ALL_IN_ONE_CONTEXT_CONFIG_KEY: False,
    # The timespan in minutes in which a chat will be kept active after the last message
    telegram_bot.CHAT_LIFETIME: 5
}

with Module(
        name=telegram_bot.MODULE_NAME,
        config=CONFIG,
        depends=(rawio.mod, interloc.mod, ontology.mod, emotion.mod)) as mod:

    mod.add(telegram_bot.telegram_run)
    mod.add(telegram_bot.telegram_output)
    mod.add(telegram_bot.show_shy)
    mod.add(telegram_bot.show_surprise)
    mod.add(telegram_bot.show_happy)
    mod.add(telegram_bot.show_affectionate)
