import os, sys
from threading import Thread

from pyrogram import Client, filters
from config import API_ID, API_HASH, TOKEN, sudofilter


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


@bot.on_message(filters.command("r") & sudofilter & ~filters.forwarded & ~filters.group & ~filters.edited & ~filters.via_bot)
async def restart(bot, message):
    Thread(
        target=stop_and_restart
    ).start()


@bot.on_message(filters.command("getbotdb") & sudofilter & ~filters.forwarded & ~filters.group & ~filters.edited & ~filters.via_bot)
async def send_the_db(bot, message):
 await message.reply_document("userlanguages.db", thumb("botprofilepic.jpg"))
    
    
bot.run()
