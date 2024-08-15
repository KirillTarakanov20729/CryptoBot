from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


PaymentMethodKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Sber")],
        [KeyboardButton(text="Alfa-bank")],
        [KeyboardButton(text="Tincoff")],
    ],
    resize_keyboard=True
)