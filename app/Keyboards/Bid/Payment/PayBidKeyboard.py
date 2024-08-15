from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


PayBidKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я оплатил сделку", callback_data="pay_bid")],
        [InlineKeyboardButton(text="Отменить сделку", callback_data="cancel_bid")]
    ])
