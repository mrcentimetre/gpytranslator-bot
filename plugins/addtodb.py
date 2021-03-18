from pyrogram import Client, filters
from pyrogram.types import Message
from db import functions as db

@Client.on_message(filters.private, group=-1)
async def check_chat(bot: Client, message: Message):
    chat_id = message.chat.id
    chat_type = message.chat.type

    if not db.chat_exists(chat_id, chat_type):
        db.add_chat(chat_id, chat_type)
        db.set_lang(chat_id, chat_type, "en")
