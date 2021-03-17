from pyrogram import Client, filters
from pyrogram.types import Message
import pytesseract, PIL, os
import constants

@Client.on_message(filters.command("ocr"))
async def ocrcmd(bot, message: Message):
 if not message.reply_to_message:
  await message.reply(constants.error_ocr_no_reply)
  return
 if not message.reply_to_message.photo:
  await message.reply(constants.error_ocr_no_reply)
  return
 if message.reply_to_message.photo:
    await message.reply_to_message.download(file_name='ocr.jpg')
    await message.reply(constants.ocr_message_text.format(pytesseract.image_to_string(PIL.Image.open('downloads/ocr.jpg'))))
    os.remove("downloads/ocr.jpg")
