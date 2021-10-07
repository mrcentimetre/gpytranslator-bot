from .db import users


async def add_chat(chat_id):
    await users.create(user_id=chat_id, chat_lang="en")


async def chat_exists(chat_id):
    return await users.exists(user_id=chat_id)


async def get_lang(chat_id: int) -> str:
    return (await users.get(user_id=chat_id)).chat_lang


async def set_lang(chat_id: int, lang_code: str):
    await users.filter(user_id=chat_id).update(chat_lang=lang_code)


async def get_users_count():
    return await users.all().count()
