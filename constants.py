from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

default_lang = "en"

start_message_text = """
Hello {} \U0001F60E I am GpyTranslatorBot AKA Gipy \ud83e\udd16

Send any text which you would like to translate for English.

**Available commands:**
/donate - Support developers
/help - Show this help message
/language - Set your main language

If you have questions about this bot or bots' development__ -  Feel free to put your question in @TDICSupport

Enjoy! ☺"""

start_message_reply_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ Add me to a Group ➕",  url="http://t.me/GpyTranslatorBot?startgroup=tr")
        ],
        [
            InlineKeyboardButton(  
                        "🔍 Inline here",
                        switch_inline_query_current_chat=" "
                    ),
            InlineKeyboardButton(
                "📄 Source code",  url="https://github.com/mrcentimetre/gpytranslator-bot"),
        ],
        [
            InlineKeyboardButton(
                "🆘 Help",  callback_data="help"),
            InlineKeyboardButton(
                "Credits 💚",  callback_data=b"Credits")
        ],
        [
            InlineKeyboardButton(
                "📣 Channel",  url="https://t.me/TDICProjects"),
            InlineKeyboardButton(
                "Group 👥",  url="https://t.me/TDICSupport"),
        ]
    ]
)

help_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔙 Back", callback_data="back")],
            ]
        )

credits = """Development 🧑‍💻
 • @MrCentimetre
 • @itayki
 • @rojserbest

Inspiration 👨🏻‍🏫
 • @DavideGalilei"""

help_text = """
**GpyTranslate Bot**

GpyTranslate is a word 'G+Py+Translate' which means 'Google Python Translate'. A bot to help you translate text (with emojis) to few Languages from any other language in world.

GpyTranslator Bot is able to detect a wide variety of languages because he is a grand son of Google Translate API.

You can use GpyTranslator Bot in his private chat. But GpyTranslator Bot is not available for Telegram Group & Channel.

**How To**
Just send copied text or forward message with other language to GpyTranslator Bot and you'll receive a translation of the message in the language of your choice. Send /language command to know which language is available.

****More help****

**Groups**
/tr (language) by reply to translate the replied message

**Translate in private chat without change the main language**
/tr (language) (text)

**Translate in inline mode**
@GpyTranslatorBot (language) (text)

---
Find a problem? Send to @MrCentimetre

coded by @MrCentimetreLK and @itayki by using @DavideGalilei's Library with 💚
"""

donate_text = """
It's just a command \ud83d\ude09 But you can contact me - @MrCentimetre
"""

language_text = """
**Languages**

__Select the language you want to translate.__

•/lang (language code) 

Example: ```/lang en``` 

List of language codes: https://cloud.google.com/translate/docs/languages


"""

error_ocr_no_reply = """reply to a photo to get the text"""

lang_saved_message = """{} has been set as your main language."""

ocr_message_text = """```the text in the image:``` \n\n {}"""

translate_string_one = """**\ud83c\udf10 Translation**:\n\n```{}```\n\n**🔍 Detected language:** {} \n\n **Translated to**: {}"""

translate_string_two = """**\ud83c\udf10 Translation**:\n\n```{}```\n\n**🔍 Detected language:** {}"""

inline_text_string_one = """Translate from {} to {}"""
