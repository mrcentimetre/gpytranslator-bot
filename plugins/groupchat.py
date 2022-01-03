from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import constants
from tr import tr
from bot_errors_logger import logging_errors
from bot_custom_exceptions import google_api_error
from gpytranslate import TranslationError

prefix = constants.prefix


@Client.on_message(filters.command("poll", prefix) & filters.group & filters.reply)
@logging_errors
async def gen_poll_tr_group_chat(bot, message: Message):
    try:
        if message.reply_to_message.poll:
            replymsg = message.reply_to_message
            poll_options = "\n".join(i["text"] for i in replymsg.poll.options)
            txt_to_tr = f"{replymsg.poll.question}\n{poll_options}"
            if len(message.text.split()) > 1:
                tolanguage = message.command[1]
            else:
                tolanguage = "en"
            translation = await tr(txt_to_tr, targetlang=[tolanguage, "utf-16"])
            translation_text = translation.text
            poll_que = translation_text.split("\n", 1)[0]
            poll_opt = translation_text.splitlines()[1:]
            return await bot.send_poll(
                chat_id=message.chat.id,
                question=poll_que,
                options=poll_opt,
                is_anonymous=replymsg.poll.is_anonymous,
                allows_multiple_answers=replymsg.poll.allows_multiple_answers,
            )
        else:
            return
    except TranslationError:
        raise google_api_error(constants.google_tr_api_err_msg)


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
            else:
                return
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
    except TranslationError:
        raise google_api_error(constants.google_tr_api_err_msg)


@Client.on_message(filters.command("tr", prefix) & filters.group & ~filters.reply)
@logging_errors
async def translategrouptwo(bot, message: Message):
    try:
        if len(message.text.split()) > 1:
            tolanguage = message.command[1]
        else:
            return await message.reply_text(constants.err_must_specify_lang)
        if len(message.text.split()) > 2:
            to_translate = message.text.split(None, 2)[2]
        else:
            return await message.reply_text(constants.err_must_specify_text)
        language = await tr.detect(message.text.split(None, 2)[2])
        translation = await tr(to_translate, sourcelang=language, targetlang=tolanguage)
        await message.reply_text(
            constants.translate_string_one.format(
                translation.text, language, tolanguage
            ),
            parse_mode="markdown",
        )
    except TranslationError:
        raise google_api_error(constants.google_tr_api_err_msg)


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
