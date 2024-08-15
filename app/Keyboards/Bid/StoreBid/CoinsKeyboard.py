from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


CoinsKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="BTC"), KeyboardButton(text="ETH")],
        [KeyboardButton(text="SOL"), KeyboardButton(text="BNB")]
    ],
    resize_keyboard=True
)