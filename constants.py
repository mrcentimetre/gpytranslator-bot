from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


prefix: list = ["/", "!", "#", "."]


start_message_text: str = """
Hello {} \U0001F60E I am GpyTranslatorBot AKA Gipy \ud83e\udd16

Send any text or poll which you would like to translate for another language.

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
                "➕ Add me to a Group ➕",
                url="http://t.me/GpyTranslatorBot?startgroup=tr",
            )
        ],
        [
            InlineKeyboardButton("🔍 Inline here", switch_inline_query_current_chat=" "),
            InlineKeyboardButton(
                "💳 Donate", url="https://www.paypal.com/paypalme/itayki"
            ),
        ],
        [
            InlineKeyboardButton("🆘 Help", callback_data="help"),
            InlineKeyboardButton("Credits 💚", callback_data=b"Credits"),
        ],
        [
            InlineKeyboardButton("📣 Channel", url="https://t.me/TDICProjects"),
            InlineKeyboardButton("Group 👥", url="https://t.me/TDICSupport"),
        ],
    ]
)

help_markup = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🔙 Back", callback_data="back")],
    ]
)

error_message_markup = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🗑 Delete this message", callback_data="closethismsg")],
    ]
)


credits: str = """Development 🧑‍💻
 • @MrCentimetre
 • @itayki
 • @rojserbest

Inspiration 👨🏻‍🏫
 • @DavideGalilei"""

help_text: str = """
**GpyTranslate Bot**
GpyTranslate is a word 'G+Py+Translate' which means 'Google Python Translate'. A bot to help you translate text (with emojis) & POLLS to one language from any other language in world.
GpyTranslator Bot is able to detect a wide variety of languages because he is a grand son of Google Translate API.
You can use GpyTranslator Bot in private chat, groups and inline mode. Also you can use /ocr command to get a text from an image and /poll command to translate poll as a poll.

**How To**
Just send copied text or forward message with other language to GpyTranslator Bot and you'll receive a translation of the message in the language of your choice. You can also translate quiz and polls. Send /language command to know which language is available.

**More help \u2699\ufe0f**

\ud83d\udccc **Groups & Privat Chat Commands**
• **Translate**
   - /tr (language code (ISO 639-1)) - Translate replied message
   - /tr (language code (ISO 639-1)) (text) - Translate to another language without changing main language
   - /poll (language code (ISO 639-1)) - Translate replied poll as a poll

• **OCR**
  - /ocr - To get text from image. (Text of the image must to be in English, else use /ocrlang.)
  - /ocrlang (language code (ISO 639-2)) - To get text from image. (Laguage parameter is the language of the text in the image)

* Note: First you should send ab image and then send /ocr as a reply.
    
• **Set Your Default Language (Private Only)**
 - /lang (language code (ISO 639-1)) - Set your default language

\ud83d\udccc **Translate With Inline Mode**
 - @GpyTranslatorBot (language code (ISO 639-1)) (text)


__If you do not specify any language code, the given text will be translated to English.__
More Info about Language Codes - https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
---
Find a problem? Send to @MrCentimetre
coded by @MrCentimetreLK and @itayki by using @DavideGalilei's Library with 💚
"""

donate_text: str = """
Donations: https://www.paypal.com/paypalme/itayki
"""

language_text: str = """
**Languages**

__Select the language you want to translate.__

•/lang (language code) 

Example: ```/lang en``` 

List of language codes: https://cloud.google.com/translate/docs/languages


"""

error_ocr_no_reply: str = """Reply to a photo to get the text"""

lang_saved_message: str = """{} has been set as your main language."""

ocr_message_text: str = """```Text in the image:``` \n\n {}"""

translate_string_one: str = """**\ud83c\udf10 Translation**:\n\n```{}```\n\n**🔍 Detected language:** {} \n\n **Translated to**: {}"""

translate_string_two: str = (
    """**\ud83c\udf10 Translation**:\n\n```{}```\n\n**🔍 Detected language:** {}"""
)

inline_text_string_one: str = """Translate from {} to {}"""

error_msg_string: str = """**Error:**  \n\n ```{}``` \n\n **Forward this message to https://t.me/TDICSupport if you see this error again, try to forward your message too for better help**"""

help_group_string: str = """To get help click on the button below"""


google_tr_api_err_msg: str = """Google has limited Translate API: Please Try Again Later."""

ocr_err_msg_lang: str = """This language code isn't supported in the ocr. Try to find correct language code by clicking this link {}"""

err_must_specify_lang = """You must specify the language to translate."""

err_must_specify_text = """You must specify the text to translate."""
