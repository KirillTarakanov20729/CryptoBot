from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


CurrencyKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="USD")],
        [KeyboardButton(text="EUR")],
        [KeyboardButton(text="RUB")]
    ],
    resize_keyboard=True
)