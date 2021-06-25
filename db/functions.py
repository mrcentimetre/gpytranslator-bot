from .db import users


async def add_chat(chat_id, chat_type):
    if chat_type == "private":
        await users.create(user_id=chat_id, chat_lang="en")


async def chat_exists(chat_id, chat_type):
    if chat_type == "private":
        return await users.exists(user_id=chat_id)


async def get_lang(chat_id: int, chat_type: str) -> str:
    if chat_type == "private":
        return (await users.get(user_id=chat_id)).chat_lang


async def set_lang(chat_id: int, chat_type: str, lang_code: str):
    if chat_type == "private":
        await users.filter(user_id=chat_id).update(chat_lang=lang_code)


async def get_users_count():
    return await users.all().count()
