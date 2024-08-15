from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


CompleteBidKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить сделку", callback_data="complete_bid")]
    ])
