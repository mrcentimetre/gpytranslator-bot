from pyrogram import Client, filters
from gpytranslate import Translator
import string

lang = 'en'

bot = Client(
    "APP_NAME",
    api_id=API_ID,
    api_hash="API_HASH",
    bot_token= "TOKEN"
)

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
async def si(bot, msg):
    global lang
    lang = msg.command[1]
    @bot.on_message(filters.private & filters.private)
    async def main(bot, msg):
        tr = Translator()
        translation = await tr(msg.text, targetlang=[lang, 'utf-16'])
        language = await tr.detect(msg.text)
        await msg.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")



##main translation process
@bot.on_message(filters.private)
async def main(bot, msg):
    tr = Translator()
    translation = await tr(msg.text, targetlang=[lang, 'utf-16'])
    language = await tr.detect(msg.text)
    await msg.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")




bot.run()
