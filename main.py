from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputTextMessageContent, InlineQueryResultArticle
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

#Get User IDs and save it in DB
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
        
@bot.on_callback_query(filters.regex(r"^back"))
async def backtostart(bot, query: CallbackQuery):
 await query.message.edit(f"Hello {query.from_user.mention} \U0001F60E I am GpyTranslatorBot AKA Gipy \ud83e\udd16 \n\nSend any text which you would like to translate for English.\n\n**Available commands:**\n/donate - Support developers\n/help - Show this help message\n/language - Set your main language\n\n__If you have questions about this bot or bots' development__ - Contact @MrCentimetreLK\n\nEnjoy! ☺",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to a Group ➕",  url="http://t.me/GpyTranslatorBot?startgroup=tr")
                ],
                [
                    InlineKeyboardButton("🆘 Help",  callback_data="help"),
                    InlineKeyboardButton("💚 Credits",  callback_data=b"Credits")
                ],
                [
                    InlineKeyboardButton("📣 Channel",  url="https://t.me/CentiProjects"),
                    InlineKeyboardButton("👥 Group",  url="https://t.me/joinchat/VBrSurucLQFgJ_r2"),
                ]
            ]
        )
    )
    
##Buttons
@bot.on_message(filters.command("start") & filters.private)
async def welcomemsg(bot, msg):
    await msg.reply(f"Hello {msg.from_user.mention} \U0001F60E I am GpyTranslatorBot AKA Gipy \ud83e\udd16 \n\nSend any text which you would like to translate for English.\n\n**Available commands:**\n/donate - Support developers\n/help - Show this help message\n/language - Set your main language\n\n__If you have questions about this bot or bots' development__ - Contact @MrCentimetreLK\n\nEnjoy! ☺",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to a Group ➕",  url="http://t.me/GpyTranslatorBot?startgroup=tr")
                ],
                [
                    InlineKeyboardButton("🆘 Help",  callback_data="help"),
                    InlineKeyboardButton("💚 Credits",  callback_data=b"Credits")
                ],
                [
                    InlineKeyboardButton("📣 Channel",  url="https://t.me/CentiProjects"),
                    InlineKeyboardButton("👥 Group",  url="https://t.me/joinchat/VBrSurucLQFgJ_r2"),
                ]
            ]
        )
    )
#Setup Help Message with buttons    
@bot.on_callback_query(filters.regex(r"^help"))
async def helpbutton(bot: Client, query: CallbackQuery):
    await query.message.edit("**GpyTranslate Bot**\n\nGpyTranslate is a word 'G+Py+Translate' which means 'Google Python Translate'. A bot to help you translate text (with emojis) to few Languages from any other language in world.\n\nGpyTranslator Bot is able to detect a wide variety of languages because he is a grand son of Google Translate API.\n\nYou can use GpyTranslator Bot in his private chat. But GpyTranslator Bot is not available for Telegram Group & Channel.\n\n**How To**\nJust send copied text or forward message with other language to GpyTranslator Bot and you'll receive a translation of the message in the language of your choice. Send /language command to know which language is available.\n\n---\nFind a problem? Send to @MrCentimetre\n\ncoded by @MrCentimetreLK and @itayki by using @DavideGalilei 's Library with 💚",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔙 Back", callback_data="back")],
            ]
        )
    )

#Popup Credits    
@bot.on_callback_query(filters.regex(r"^Credits"))
async def credits(bot: Client, query: CallbackQuery):
    await query.answer("Developers 🧑‍💻\n\n • @MrCentimetreLK\n • @itayki\n\nInspiration 👨🏻‍🏫\n\n • @DavideGalilei", show_alert=True)
    
##Configure welcome message
@bot.on_message(filters.command("hi") & filters.private)
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
@bot.on_message(filters.private & ~filters.command("tr"))
async def main(bot, msg):
    tr = Translator()
    userlang = get_db_lang(msg.chat.id, msg.chat.type)
    translation = await tr(msg.text, targetlang=[userlang, 'utf-16'])
    language = await tr.detect(msg.text)
    await msg.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")
    
@bot.on_message(filters.command("tr") & filters.group)
async def translategroup(bot, msg) -> None:
    tr = Translator()
    if not msg.reply_to_message:
        await msg.reply("Reply to a message to translate")
        return
    if msg.reply_to_message.caption:
        to_translate = msg.reply_to_message.caption
    elif msg.reply_to_message.text:
        to_translate = msg.reply_to_message.text
    try:
        args = msg.text.split()[1].lower()
        if "//" in args:
            language = args.split("//")[0]
            tolanguage = args.split("//")[1]
        else:
            language = await tr.detect(to_translate)
            tolanguage = args
    except IndexError:
        language = await tr.detect(to_translate)
        tolanguage = "en"
    translation = await tr(to_translate,
                              sourcelang=language, targetlang=tolanguage)
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}" 
    await msg.reply(trmsgtext, parse_mode="markdown")

@bot.on_message(filters.command("tr") & filters.private)
async def translateprivatetwo(bot, msg) -> None:
    tr = Translator()
    to_translate = msg.text.split(None, 2)[2]
    language = await tr.detect(msg.text.split(None, 2)[2])
    tolanguage = msg.command[1]
    translation = await tr(to_translate,
                              sourcelang=language, targetlang=tolanguage)
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}" 
    await msg.reply(trmsgtext, parse_mode="markdown")

#Inline Bot
@bot.on_inline_query()
async def translateinline(bot, query) -> None:
 try:
    tr = Translator()
    to_translate = query.query.lower().split(None, 1)[1]
    language = await tr.detect(query.query.lower().split(None, 1)[1])
    tolanguage = query.query.lower().split()[0]
    translation = await tr(to_translate,
                              sourcelang=language, targetlang=tolanguage)
    trmsgtext =f"{translation.text}" 
    await query.answer([InlineQueryResultArticle(
       title= f"Translate from {language} to {tolanguage}",description=f"{translation.text}",input_message_content=InputTextMessageContent(trmsgtext)
    )])
 except IndexError:
  return
    
bot.run()
