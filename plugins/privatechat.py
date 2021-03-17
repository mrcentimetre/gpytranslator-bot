from pyrogram import Client, filters
from pyrogram.types import Message

import constants
import db
from tr import tr


@Client.on_message(
    filters.command("start")
    & filters.private
)
async def start(bot, message: Message):
 if len(message.text.split()) > 1:
  if message.command[1] == "help":
    await message.reply_text(constants.help_text)
 else:
    await message.reply_text(constants.start_message_text.format(message.from_user.mention()), reply_markup=constants.start_message_reply_markup)


@Client.on_message(
    filters.command("help")
    & filters.private
)
async def help(bot, message: Message):
    await message.reply_text(constants.help_text)


@Client.on_message(
    filters.command("donate")
    & filters.private
)
async def donate(bot, message: Message):
    await message.reply_text(constants.donate_text)


@Client.on_message(filters.command("language"))
async def language(bot, message: Message):
    await message.reply_text(constants.language_text)


@Client.on_message(filters.command("lang") & filters.private)
async def setmylang(bot, message: Message):
    thelang = message.command[1]
    await message.reply(constants.lang_saved_message.format(thelang))
    db.set_lang(message.chat.id, message.chat.type, thelang)


@Client.on_message(filters.private & ~filters.command("tr") & ~filters.command("start"))
async def main(bot, message: Message):
    userlang = db.get_lang(message.chat.id, message.chat.type)
    translation = await tr(message.text, targetlang=[userlang, 'utf-16'])
    language = await tr.detect(message.text)
    await message.reply(constants.translate_string_two.format(translation.text, language))


@Client.on_message(filters.command("tr") & filters.private)
async def translateprivatetwo(bot, message: Message):
    to_translate = message.text.split(None, 2)[2]
    language = await tr.detect(message.text.split(None, 2)[2])
    tolanguage = message.command[1]
    translation = await tr(to_translate,
                           sourcelang=language, targetlang=tolanguage)
    await message.reply(constants.translate_string_one.format(translation.text, language, tolanguage), parse_mode="markdown")
