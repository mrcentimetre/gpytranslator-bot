from pyrogram import Client
from pyrogram.types import Message, InlineQuery
from functools import wraps
import constants

def logging_errors(f):
    @wraps(f)
    async def err_log(client: Client, message: Message, *args, **kwargs):
        try:
            return await f(client, message, *args, **kwargs)
        except Exception as e:
            await message.reply(f"**Error:**  \n\n ```{e}``` \n\n **forward this message to https://t.me/TDICSupport if you see this error again**", parse_mode="markdown", reply_markup=constants.error_message_markup)
    return err_log
