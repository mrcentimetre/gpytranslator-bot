from pyrogram import Client, enums
from pyrogram.types import Message
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
                await message.reply(
                    constants.error_msg_string.format(f"{type(e).__name__}: {e}"),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=constants.error_message_markup,
                    disable_web_page_preview=True,
                )
            except ChatWriteForbidden:
                await message.chat.leave()
                return

    return err_log
