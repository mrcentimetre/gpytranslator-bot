from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from functools import wraps
import constants
import json


def logging_errors(f):
    @wraps(f)
    async def err_log(client: Client, message: Message, *args, **kwargs):
        try:
            return await f(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await message.chat.leave()
            return
        except json.decoder.JSONDecodeError:
            await message.reply(constants.google_tr_api_err_msg, parse_mode="markdown")
        except Exception as e:
            try:
                await message.reply(
                    constants.error_msg_string.format(e),
                    parse_mode="markdown",
                    reply_markup=constants.error_message_markup,
                )
            except ChatWriteForbidden:
                await message.chat.leave()
                return

    return err_log
