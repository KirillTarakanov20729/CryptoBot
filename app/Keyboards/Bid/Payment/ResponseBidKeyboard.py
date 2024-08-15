from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ResponseBidKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я согласен провести сделку", callback_data="response_bid")],
        [InlineKeyboardButton(text="Отменить сделку", callback_data="cancel_bid")]
    ])
