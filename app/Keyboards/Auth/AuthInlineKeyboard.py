from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


AuthInlineKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вход", callback_data="login")],
        [InlineKeyboardButton(text="Регистрация", callback_data="reg")],
    ])