from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


DeleteKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить заявку", callback_data="delete_bid")],
    ])
