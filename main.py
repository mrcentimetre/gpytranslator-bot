import os
import sys
from threading import Thread

from pyrogram import Client, filters
from config import API_ID, API_HASH, TOKEN


bot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="plugins")
)


def stop_and_restart():
    bot.stop()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command("r") & filters.user("itayki"))
async def restart(bot, message):
    Thread(
        target=stop_and_restart
    ).start()

bot.run()
