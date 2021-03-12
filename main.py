import os
import sys
from threading import Thread

from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, SUDO_FILTER

bot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)


def stop_and_restart():
    bot.stop()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(
    filters.command("r")
    & SUDO_FILTER
    & ~ filters.forwarded
    & ~ filters.group
    & ~ filters.edited
    & ~ filters.via_bot
)
async def restart(_, __):
    Thread(
        target=stop_and_restart
    ).start()


bot.run()
