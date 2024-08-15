from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ReplyContactKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
    ],
    resize_keyboard=True
)
