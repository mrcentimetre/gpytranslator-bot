from pyrogram import Client, filters
from pyrogram.types import Message
from db import functions as db


@Client.on_message(filters.private, group=-1)
async def check_chat(bot: Client, message: Message):
    chat_id = message.chat.id
    check_if_chat_exists = await db.chat_exists(chat_id)
    if not check_if_chat_exists:
        await db.add_chat(chat_id)
        await db.set_lang(chat_id, "en")
