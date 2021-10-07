from config import MESSAGES, SECONDS, USERS, BANNED_USERS
from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Union
from time import time


def is_flood(uid: int) -> Union[bool, None]:
    """Checks if a user is flooding"""

    USERS[uid].append(time())
    if len(list(filter(lambda x: time() - int(x) < SECONDS, USERS[uid]))) > MESSAGES:
        USERS[uid] = list(filter(lambda x: time() - int(x) < SECONDS, USERS[uid]))
        return True


@Client.on_message(filters.private | filters.group, group=-100)
def antiflood(_: Client, msg: Message):
    if is_flood(msg.from_user.id):
        BANNED_USERS.add(msg.from_user.id)
    elif msg.from_user.id in BANNED_USERS:
        BANNED_USERS.remove(msg.from_user.id)
