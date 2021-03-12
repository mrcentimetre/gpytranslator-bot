from typing import Union
from . import database

user_languages = database.user_languages


async def get_user_language(chat_id: int) -> Union[str, None]:
    find = await user_languages.find_one({"chat_id": chat_id})

    if find:
        return find["language"]


async def update_user_language(chat_id: int, language: str):
    await user_languages.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "language": language
            }
        },
        upsert=True
    )
