from pyrogram import Client
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import constants

from tr import tr


@Client.on_inline_query()
async def translateinline(bot: Client, query: InlineQuery) -> None:
    try:
        to_translate = query.query.lower().split(None, 1)[1]
        language = await tr.detect(query.query.lower().split(None, 1)[1])
        tolanguage = query.query.lower().split()[0]
        translation = await tr(
            to_translate,
            sourcelang=language,
            targetlang=tolanguage
        )
        trmsgtext = f"{translation.text}"
        await query.answer(
            [
                InlineQueryResultArticle(
                    title=constants.inline_text_string_one.format(language, tolanguage),
                    description=f"{translation.text}",
                    input_message_content=InputTextMessageContent(trmsgtext)
                )
            ]
        )
    except IndexError:
        return
