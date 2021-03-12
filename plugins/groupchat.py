from pyrogram import Client, filters
from pyrogram.types import Message

from tr import tr


@Client.on_message(
    filters.command("tr")
    & filters.group
)
async def translate_group(bot, message: Message) -> None:
    if not message.reply_to_message:
        await message.reply("Reply to a message to translate")
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
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}"
    await message.reply(trmsgtext, parse_mode="markdown")
