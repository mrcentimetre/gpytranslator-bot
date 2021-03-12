from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
DB_URI = getenv("DB_URI")
DB_NAME = getenv("DB_NAME")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
SUDO_FILTER = filters.user(SUDO_USERS)
