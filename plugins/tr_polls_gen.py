from pyrogram import Client, filters
from pyrogram.types import Message
from bot_errors_logger import logging_errors
import constants
import db
from tr import tr
import json
from bot_custom_exceptions import google_api_error

prefix = constants.prefix


@Client.on_message(
    filters.command("tr_poll_gen", prefix) & filters.private & filters.reply
)
@logging_errors
async def gen_poll_tr_private_chat(bot, message: Message):
    try:
        if message.reply_to_message.poll:
            replymsg = message.reply_to_message
            poll_options = "\n".join(i["text"] for i in replymsg.poll.options)
            txt_to_tr = f"{replymsg.poll.question}\n{options}"
            if len(message.text.split()) > 1:
                tolanguage = message.command[1]
            else:
                tolanguage = await db.get_lang(message.chat.id, message.chat.type)
            translation = await tr(txt_to_tr, targetlang=[userlang, "utf-16"])
            translation_text = translation.text
            poll_que = translation_text.split("\n", 1)[0]
            poll_opt = translation_text.splitlines()[1:]
            return await bot.send_poll(
                chat_id=message.chat.id,
                question=poll_que,
                options=poll_opt,
                is_anonymous=replymsg.poll.is_anonymous,
                allows_multiple_answers=replymsg.poll.allows_multiple_answers,
            )
        else:
            return
    except json.decoder.JSONDecodeError:
        raise google_api_error(constants.google_tr_api_err_msg)
