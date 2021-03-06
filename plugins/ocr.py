from pyrogram import Client, filters
from pyrogram.types import Message
import pytesseract, PIL, os

@Client.on_message(filters.command("ocr"))
async def ocrcmd(bot, message: Message):
 if not message.reply_to_message:
  await message.reply("reply to a photo to get the text")
  return
 if not message.reply_to_message.photo:
  await message.reply("reply to a photo to get the text")
  return
 if message.reply_to_message.photo:
    await message.reply_to_message.download(file_name='ocr.jpg')
    await message.reply(f"```the text from in the image:``` \n\n {pytesseract.image_to_string(PIL.Image.open('downloads/ocr.jpg'))}")
    os.remove("downloads/ocr.jpg")
