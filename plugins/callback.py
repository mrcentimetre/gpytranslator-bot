from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from bot_errors_logger import logging_errors
import constants


@Client.on_callback_query(filters.regex(r"^back"))
@logging_errors
async def backtostart(bot: Client, query: CallbackQuery):
    await query.message.edit(
        constants.start_message_text.format(query.from_user.mention()),
        reply_markup=constants.start_message_reply_markup
    )


@Client.on_callback_query(filters.regex(r"^help"))
@logging_errors
async def helpbutton(bot: Client, query: CallbackQuery):
    await query.message.edit(
        constants.help_text,
        reply_markup=constants.help_markup
    )


@Client.on_callback_query(filters.regex(r"^Credits"))
@logging_errors
async def credits(bot: Client, query: CallbackQuery):
    await query.answer(constants.credits, show_alert=True)
