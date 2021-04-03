from pyrogram import Client, filters
from config import API_ID, API_HASH, TOKEN, sudofilter


bot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="plugins")
)


bot.run()
