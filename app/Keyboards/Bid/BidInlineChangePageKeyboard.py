from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


FirstPageInlineKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Следующая страница", callback_data="next_page")],
        [InlineKeyboardButton(text="Последняя страница", callback_data="last_page")],
    ])


MidPageInlineKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Первая страница", callback_data="first_page")],
        [InlineKeyboardButton(text="Предыдущая страница", callback_data="previous_page")],
        [InlineKeyboardButton(text="Следующая страница", callback_data="next_page")],
        [InlineKeyboardButton(text="Последняя страница", callback_data="last_page")],
    ])

LastPageInlineKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Первая страница", callback_data="first_page")],
        [InlineKeyboardButton(text="Предыдущая страница", callback_data="previous_page")],
    ])
