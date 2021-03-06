from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputTextMessageContent,
    InlineQueryResultArticle
)

from gpytranslate import Translator
from pyrogram.types.messages_and_media.message import Message

import db
import constants

bot = Client(
    ":memory:",
    api_id=1,
    api_hash="abcdefghijklnmnopqrstuv",
    bot_token="123456:abcdefghijklnmnopqrstuv"
)

default_language = "en"


@bot.on_message(filters.private, group=-1)
async def check_chat(bot, msg):
    chat_id = msg.chat.id
    chat_type = msg.chat.type

    if not db.chat_exists(chat_id, chat_type):
        db.add_chat(chat_id, chat_type)
        db.set_lang(chat_id, chat_type, "en")


@bot.on_callback_query(filters.regex(r"^back"))
async def backtostart(bot, query: CallbackQuery):
    await query.message.edit(constants.start_message_text.format(query.from_user.mention()), reply_markup=constants.start_message_reply_markup)


@bot.on_message(filters.command("start") & filters.private)
async def welcomemsg(bot, msg):
    await msg.reply(constants.start_message_text, reply_markup=constants.start_message_reply_markup)


@bot.on_callback_query(filters.regex(r"^help"))
async def helpbutton(bot: Client, query: CallbackQuery):
    await query.message.edit(constants.start_message_text, reply_markup=constants.start_message_reply_markup)


@bot.on_callback_query(filters.regex(r"^Credits"))
async def credits(bot: Client, query: CallbackQuery):
    await query.answer(constants.credits, show_alert=True)


@bot.on_message(filters.command("hi") & filters.private)
async def start(bot, msg):
    await msg.reply_text(constants.start_message_text.format(msg.from_user.mention()))


@bot.on_message(filters.private & filters.command("help"))
async def help(bot, msg):
    await msg.reply_text(constants.help_text)


@bot.on_message(filters.private & filters.command("donate"))
async def donate(bot, msg):
    await msg.reply_text(constants.donate_text)


@bot.on_message(filters.private & filters.command("language"))
async def language(bot, msg):
    await msg.reply_text(constants.language_text)


@bot.on_message(filters.command("lang") & filters.private)
async def setmylang(bot, msg):
    thelang = msg.command[1]
    await msg.reply(f"{thelang} has been set as your main language.")
    db.set_lang(msg.chat.id, msg.chat.type, thelang)


@bot.on_message(filters.private & ~filters.command("tr"))
async def main(bot, msg):
    tr = Translator()
    userlang = db.get_lang(msg.chat.id, msg.chat.type)
    translation = await tr(msg.text, targetlang=[userlang, 'utf-16'])
    language = await tr.detect(msg.text)
    await msg.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")


@ bot.on_message(filters.command("tr") & filters.group)
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


@ bot.on_message(filters.command("tr") & filters.private)
async def translateprivatetwo(bot, msg) -> None:
    tr = Translator()
    to_translate = msg.text.split(None, 2)[2]
    language = await tr.detect(msg.text.split(None, 2)[2])
    tolanguage = msg.command[1]
    translation = await tr(to_translate,
                           sourcelang=language, targetlang=tolanguage)
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}"
    await msg.reply(trmsgtext, parse_mode="markdown")

# Inline Bot


@ bot.on_inline_query()
async def translateinline(bot, query) -> None:
    try:
        tr = Translator()
        to_translate = query.query.lower().split(None, 1)[1]
        language = await tr.detect(query.query.lower().split(None, 1)[1])
        tolanguage = query.query.lower().split()[0]
        translation = await tr(to_translate,
                               sourcelang=language, targetlang=tolanguage)
        trmsgtext = f"{translation.text}"
        await query.answer([InlineQueryResultArticle(
            title=f"Translate from {language} to {tolanguage}", description=f"{translation.text}", input_message_content=InputTextMessageContent(trmsgtext)
        )])
    except IndexError:
        return

bot.run()
