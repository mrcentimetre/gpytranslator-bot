from pyrogram import Client
from pyrogram.types import Message, InlineQuery
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from functools import wraps
import constants

def logging_errors(f):
    @wraps(f)
    async def err_log(client: Client, message: Message, *args, **kwargs):
        try:
            return await f(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await message.chat.leave()
            return
        except Exception as e:
            try:
                await message.reply(f"**Error:**  \n\n ```{e}``` \n\n **forward this message to https://t.me/TDICSupport if you see this error again**", parse_mode="markdown", reply_markup=constants.error_message_markup)
            except ChatWriteForbidden:
                await message.chat.leave()
                return
    return err_log
