from pyrogram import Client, filters, idle
from pkg_resources import get_distribution
from config import API_ID, API_HASH, TOKEN, sudofilter, db_url
import os, sys
from tortoise import run_async
from threading import Thread
from datetime import datetime
from db.db import init_db
from db.functions import get_users_count, chat_exists, get_lang
from exporter_db_to_sqlite import db_to_sqlite_func

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


@bot.on_message(filters.command("ping") & sudofilter & filters.private)
async def ping(bot, message):
    a = datetime.now()
    m = await message.reply_text("pong")
    b = datetime.now()
    await m.edit_text(f"pong {(b - a).microseconds / 1000} ms")


@bot.on_message(filters.command("bot_stats") & sudofilter)
async def get_bot_stats(bot, message):
    await message.reply(f"the bot has {await get_users_count()} users")


@bot.on_message(filters.command("get_user_lang") & sudofilter)
async def get_lang_by_user_db(bot, message):
    if len(message.text.split()) > 1:
        chat_exists_check = await chat_exists(chat_id=message.command[1])
        if chat_exists_check == True:
            await message.reply(await get_lang(chat_id=message.command[1]))
        else:
            await message.reply("¯\_(ツ)_/¯")
    else:
        await message.reply("¯\_(ツ)_/¯")


@bot.on_message(filters.command("gpytranslate_version") & sudofilter)
async def get_gpytranslate_lib_version(bot, message):
    gpytranslate_version = get_distribution("gpytranslate")
    await message.reply_text(f"gpytranslate version: {gpytranslate_version.version}")


@bot.on_message(filters.command("backup_db") & sudofilter & filters.private)
async def backup_db_cmd(bot, message):
    sqlite_output_file_name = "gpytranslatorbotdb_backup.sqlite3"
    db_to_sqlite_func(connection=db_url, path=sqlite_output_file_name)
    await message.reply_document(sqlite_output_file_name)
    os.remove(sqlite_output_file_name)


async def startbot():
    await init_db()
    await bot.start()
    await idle()


run_async(startbot())
