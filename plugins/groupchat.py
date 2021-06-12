from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import constants
from tr import tr
from bot_errors_logger import logging_errors
from bot_custom_exceptions import google_api_error

prefix = constants.prefix


@Client.on_message(
    filters.command(["tr", "tl", "translate"], prefix) & filters.group & filters.reply
)
@logging_errors
async def translategroup(bot, message: Message) -> None:
    try:
        if message.reply_to_message.poll is None:
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
            translation = await tr(
                to_translate, sourcelang=language, targetlang=tolanguage
            )
            await message.reply(
                constants.translate_string_one.format(
                    translation.text, language, tolanguage
                ),
                parse_mode="markdown",
            )
        elif message.reply_to_message.poll is not None:
            options = "\n".join(
                x["text"] for x in message.reply_to_message.poll.options
            )
            to_translate = f"{message.reply_to_message.poll.question}\n\n\n{options}"
            language = await tr.detect(to_translate)
            if len(message.text.split()) > 1:
                tolanguage = message.command[1]
            else:
                tolanguage = "en"
            translation = await tr(
                to_translate, sourcelang=language, targetlang=tolanguage
            )
            await message.reply(
                constants.translate_string_one.format(
                    translation.text, language, tolanguage
                ),
                parse_mode="markdown",
            )
    except json.decoder.JSONDecodeError:
        raise bot_custom_exceptions(constants.google_tr_api_err_msg)


@Client.on_message(filters.command("tr", prefix) & filters.group & ~filters.reply)
@logging_errors
async def translategrouptwo(bot, message: Message):
    try:
        to_translate = message.text.split(None, 2)[2]
        language = await tr.detect(message.text.split(None, 2)[2])
        tolanguage = message.command[1]
        translation = await tr(to_translate, sourcelang=language, targetlang=tolanguage)
        await message.reply(
            constants.translate_string_one.format(
                translation.text, language, tolanguage
            ),
            parse_mode="markdown",
        )
    except json.decoder.JSONDecodeError:
        raise bot_custom_exceptions(constants.google_tr_api_err_msg)


@Client.on_message(
    filters.command(["help", "help@gpytranslatorbot"], prefix) & filters.group
)
@logging_errors
async def helpgroupcmd(bot, message: Message):
    getmebot = await bot.get_me()
    await message.reply(
        constants.help_group_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🆘 Help", url=f"https://t.me/{getmebot.username}?start=help"
                    ),
                    InlineKeyboardButton(
                        "🗑 Delete this message", callback_data="closethismsg"
                    ),
                ],
            ]
        ),
    )
