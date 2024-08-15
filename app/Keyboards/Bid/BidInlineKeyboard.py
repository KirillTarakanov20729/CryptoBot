from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


BidInlineKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить запрос", callback_data="ask_bid")],
    ])
