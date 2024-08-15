from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TypesKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="sell")],
        [KeyboardButton(text="buy")],
    ],
    resize_keyboard=True
)