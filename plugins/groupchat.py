from pyrogram import Client, filters
from pyrogram.types import Message
import constants
from tr import tr


@Client.on_message(
    filters.command(["tr", "tl", "translate"])
    & filters.group
)
async def translategroup(bot, message: Message) -> None:
    if not message.reply_to_message:
        await message.reply(constants.error_group_no_reply)
        return
    if message.reply_to_message.caption:
        to_translate = message.reply_to_message.caption
    elif message.reply_to_message.text:
        to_translate = message.reply_to_message.text
    try:
        args = message.text.split()[1].lower()
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
    await message.reply(constants.translate_string_one.format(translation.text, language, tolanguage), parse_mode="markdown")
