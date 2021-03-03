from pyrogram import Client, filters
from gpytranslate import Translator
import sqlite3, string 

bot = Client(
    "APP_NAME",
    api_id=API_ID,
    api_hash="API_HASH",
    bot_token= "TOKEN"
)

db = sqlite3.connect("userlanguages.db")
dbc = db.cursor()
dbc.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,
                                                 chat_lang)""")
db.commit()

default_language = "en"

def chat_exists(chat_id, chat_type):
    if chat_type == "private":
        dbc.execute("SELECT user_id FROM users where user_id = ?", (chat_id,))
        return bool(dbc.fetchone())
    raise TypeError("Unknown chat type '%s'." % chat_type)

    
def get_db_lang(chat_id: int, chat_type: str) -> str:
    if chat_type == "private":
        dbc.execute("SELECT chat_lang FROM users WHERE user_id = ?", (chat_id,))
        ul = dbc.fetchone()
    return ul[0] if ul else None
    
def add_chat(chat_id, chat_type):
    if chat_type == "private":
        dbc.execute("INSERT INTO users (user_id) values (?)", (chat_id,))
        db.commit()
        
        
def set_db_lang(chat_id: int, chat_type: str, lang_code: str):
    if chat_type == "private":
        dbc.execute("UPDATE users SET chat_lang = ? WHERE user_id = ?", (lang_code, chat_id))
        db.commit()


        
   
@bot.on_message(filters.private, group=-1)
async def check_chat(bot, msg):
    chat_id = msg.chat.id
    chat_type = msg.chat.type

    if not chat_exists(chat_id, chat_type):
        add_chat(chat_id, chat_type)
        set_db_lang(chat_id, chat_type, "en")
        
        

    
##Configure welcome message
@bot.on_message(filters.command("start") & filters.private)
async def start(bot, msg):
    await msg.reply_text(f"Hello {msg.from_user.mention} \U0001F60E I am GpyTranslatorBot AKA Gipy \ud83e\udd16 \n\nSend any text which you would like to translate for English.\n\n**Available commands:**\n/donate - Support developers\n/help - Show this help message\n/language - Set your main language\n\n__If you have questions about this bot or bots' development__ - Contact @MrCentimetreLK\n\nEnjoy! ☺")

##When the user sent /help command, configure the message that the bot should send   
@bot.on_message(filters.private & filters.command("help"))
async def help(bot, msg):
    await msg.reply_text(f"**GpyTranslate Bot**\n\nGpyTranslate is a word 'G+Py+Translate' which means 'Google Python Translate'. A bot to help you translate text (with emojis) to few Languages from any other language in world.\n\nGpyTranslator Bot is able to detect a wide variety of languages because he is a grand son of Google Translate API.\n\nYou can use GpyTranslator Bot in his private chat. But GpyTranslator Bot is not available for Telegram Group & Channel.\n\n**How To**\nJust send copied text or forward message with other language to GpyTranslator Bot and you'll receive a translation of the message in the language of your choice. Send /language command to know which language is available.\n\n---\nFind a problem? Send to @MrCentimetre\n\ncoded by @MrCentimetreLK and @itayki by using @DavideGalilei 's Library with 💚")

##When the user sent /donate command, configure the message that the bot should send
@bot.on_message(filters.private & filters.command("donate"))
async def donate(bot, msg):
    await msg.reply_text(f"It's just a command \ud83d\ude09 But you can contact my father - @MrCentimetreLK")

##When the user sent /donate command, configure the message that the bot should send
@bot.on_message(filters.private & filters.command("language"))
async def language(bot, msg):
    await msg.reply_text(f"**Languages**\n\n__Select the language you want to translate.__\n\n•/lang (language code) \n\nExample: ```/lang en``` \n\nList of language codes: https://cloud.google.com/translate/docs/languages   \n\n Send the relevant command. \ud83e\udd20")



@bot.on_message(filters.command("lang") & filters.private)
async def setmylang(bot, msg):
 thelang = msg.command[1]
 set_db_lang(msg.chat.id, msg.chat.type, thelang)




##main translation process
@bot.on_message(filters.private)
async def main(bot, msg):
    tr = Translator()
    userlang = get_db_lang(msg.chat.id, msg.chat.type)
    translation = await tr(msg.text, targetlang=[userlang, 'utf-16'])
    language = await tr.detect(msg.text)
    await msg.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")

bot.run()
