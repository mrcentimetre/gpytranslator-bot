from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

import constants


@Client.on_callback_query(filters.regex(r"^back"))
async def backtostart(bot: Client, query: CallbackQuery):
    await query.message.edit(
        constants.start_message_text.format(query.from_user.mention()),
        reply_markup=constants.start_message_reply_markup
    )


@Client.on_callback_query(filters.regex(r"^help"))
async def helpbutton(bot: Client, query: CallbackQuery):
    await query.message.edit(
        constants.help_text,
        reply_markup=constants.help_markup
    )


@Client.on_callback_query(filters.regex(r"^Credits"))
async def credits(bot: Client, query: CallbackQuery):
    await query.answer(constants.credits, show_alert=True)
