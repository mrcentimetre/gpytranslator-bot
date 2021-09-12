from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from functools import wraps
import constants
import requests, traceback


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
                full_trace = traceback.format_exc()
                paste_req = requests.post("https://nekobin.com/api/documents", json={"content": full_trace})
                pastereqjson = paste_req.json()
                pastereqjson = pastereqjson["result"]["key"]
                paste_url = f"https://nekobin.com/{pastereqjson}"
                await message.reply(
                    constants.error_msg_string.format(f"{type(e).__name__}: {e}") + f" {paste_url}",
                    parse_mode="markdown",
                    reply_markup=constants.error_message_markup,
                )
            except ChatWriteForbidden:
                await message.chat.leave()
                return

    return err_log
