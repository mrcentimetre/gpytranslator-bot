from pyrogram import Client, filters
from config import API_ID, API_HASH, TOKEN, sudofilter
import os, sys
from threading import Thread
from datetime import datetime
from db.functions import get_users_count

bot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="plugins"),
)


def stop_and_restart():
    bot.stop()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(
    filters.command("r")
    & sudofilter
    & ~filters.forwarded
    & ~filters.group
    & ~filters.edited
    & ~filters.via_bot
)
async def restart(bot, message):
    msgtxt = await message.reply("wait")
    Thread(target=stop_and_restart).start()
    await msgtxt.edit_text("done")

@bot.on_message(
    filters.command("getbotdb")
    & sudofilter
    & ~filters.forwarded
    & ~filters.group
    & ~filters.edited
    & ~filters.via_bot
)
async def send_the_db(bot, message):
    await message.reply_document("userlanguages.db", thumb="botprofilepic.jpg")


@bot.on_message(filters.command("ping") & sudofilter & filters.private)
async def ping(bot, message):
    a = datetime.now()
    m = await message.reply_text("pong")
    b = datetime.now()
    await m.edit_text(f"pong {(b - a).microseconds / 1000} ms")


@bot.on_message(filters.command("bot_stats") & sudofilter)
async def get_bot_stats(bot, message):
    await message.reply(f"the bot have {await get_users_count()} users")


bot.run()
