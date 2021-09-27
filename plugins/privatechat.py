from pyrogram import Client, filters
from pyrogram.types import Message
from bot_errors_logger import logging_errors
import constants
import db
from tr import tr
import json
from bot_custom_exceptions import google_api_error

prefix = constants.prefix


@Client.on_message(filters.command("start", prefix) & filters.private)
@logging_errors
async def start(bot, message: Message):
    if len(message.text.split()) > 1:
        if message.command[1] == "help":
            await message.reply_text(constants.help_text)
    else:
        await message.reply_text(
            constants.start_message_text.format(message.from_user.mention()),
            reply_markup=constants.start_message_reply_markup,
        )


@Client.on_message(filters.command("help", prefix) & filters.private)
@logging_errors
async def help(bot, message: Message):
    await message.reply_text(constants.help_text)


@Client.on_message(filters.command("donate", prefix) & filters.private)
@logging_errors
async def donate(bot, message: Message):
    await message.reply_text(constants.donate_text)


@Client.on_message(filters.command("language", prefix))
@logging_errors
async def language(bot, message: Message):
    await message.reply_text(constants.language_text)


@Client.on_message(filters.command("lang", prefix) & filters.private)
@logging_errors
async def setmylang(bot, message: Message):
    if len(message.text.split()) > 1:
        thelang = message.command[1]
        await message.reply(constants.lang_saved_message.format(thelang))
        await db.set_lang(message.chat.id, thelang)
    else:
        await message.reply(constants.language_text)


@Client.on_message(filters.command("poll", prefix) & filters.private & filters.reply)
@logging_errors
async def gen_poll_tr_private_chat(bot, message: Message):
    try:
        if message.reply_to_message.poll:
            replymsg = message.reply_to_message
            poll_options = "\n".join(i["text"] for i in replymsg.poll.options)
            txt_to_tr = f"{replymsg.poll.question}\n{poll_options}"
            if len(message.text.split()) > 1:
                tolanguage = message.command[1]
            else:
                tolanguage = await db.get_lang(message.chat.id)
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
    except json.decoder.JSONDecodeError:
        raise google_api_error(constants.google_tr_api_err_msg)


@Client.on_message(
    filters.private & ~filters.command("tr", prefix) & ~filters.command("start")
)
@logging_errors
async def main(bot, message: Message):
    try:
        if message.poll is None:
            textorcaption = message.text or message.caption
            userlang = await db.get_lang(message.chat.id)
            translation = await tr(textorcaption, targetlang=[userlang, "utf-16"])
            language = await tr.detect(textorcaption or message.caption)
            await message.reply(
                constants.translate_string_two.format(translation.text, language)
            )
        elif message.poll is not None:
            userlang = await db.get_lang(message.chat.id)
            options = "\n".join(x["text"] for x in message.poll.options)
            to_translate = f"{message.poll.question}\n\n\n{options}"
            fromlang = await tr.detect(to_translate)
            translation = await tr(to_translate, targetlang=[userlang, "utf-16"])
            await message.reply(
                constants.translate_string_two.format(translation.text, fromlang),
                parse_mode="markdown",
            )
    except json.decoder.JSONDecodeError:
        raise google_api_error(constants.google_tr_api_err_msg)


@Client.on_message(filters.command("tr", prefix) & filters.private & ~filters.reply)
@logging_errors
async def translateprivatetwo(bot, message: Message):
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
        raise google_api_error(constants.google_tr_api_err_msg)


@Client.on_message(filters.command("tr", prefix) & filters.private & filters.reply)
@logging_errors
async def translateprivate_reply(bot, message: Message):
    try:
        if message.reply_to_message.poll is None:
            if message.reply_to_message.caption:
                to_translate = message.reply_to_message.caption
            elif message.reply_to_message.text:
                to_translate = message.reply_to_message.text
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
        raise google_api_error(constants.google_tr_api_err_msg)
