from pyrogram import Client, filters
from pyrogram.types import Message
import pytesseract, PIL, os
import constants
from bot_errors_logger import logging_errors
from py_multiapi import multiapi

theapi = multiapi()

prefix = constants.prefix


def getocrlangsasalist():
    a = ""
    for i in pytesseract.get_languages():
        a += f"{i}\n"
    return a


@Client.on_message(filters.command("ocr", prefix))
@logging_errors
async def ocrcmd(bot, message: Message):
    if not message.reply_to_message:
        await message.reply(constants.error_ocr_no_reply)
        return
    if not message.reply_to_message.photo:
        await message.reply(constants.error_ocr_no_reply)
        return
    if message.reply_to_message.photo:
        await message.reply_to_message.download(file_name="ocr.jpg")
        await message.reply(
            constants.ocr_message_text.format(
                pytesseract.image_to_string(PIL.Image.open("downloads/ocr.jpg"))
            )
        )
        os.remove("downloads/ocr.jpg")


@Client.on_message(filters.command("ocrlang", prefix))
@logging_errors
async def ocrlangcmd(bot, message: Message):
    if len(message.text.split()) > 1:
        msg_arg = message.command[1]
        if not message.reply_to_message:
            return await message.reply(constants.error_ocr_no_reply)
        if not message.reply_to_message.photo:
            return await message.reply(constants.error_ocr_no_reply)
        if message.reply_to_message.photo:
            if msg_arg in pytesseract.get_languages():
                await message.reply_to_message.download(file_name="ocr.jpg")
                await message.reply(
                    constants.ocr_message_text.format(
                        pytesseract.image_to_string(
                            PIL.Image.open("downloads/ocr.jpg"), lang=msg_arg
                        )
                    )
                )
                os.remove("downloads/ocr.jpg")
            else:
                ocrlangslist = getocrlangsasalist()
                thepaste = await theapi.paste(content=ocrlangslist)
                thepaste = thepaste["paste_url"]
                await message.reply(constants.ocr_err_msg_lang.format())
    else:
        await ocrcmd(bot, message)
