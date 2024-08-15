from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MainInlineKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Курс криптовалют", callback_data="coins")],
        [InlineKeyboardButton(text="Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="Заявки", callback_data="bids")],
        [InlineKeyboardButton(text="Мои заявки", callback_data="user_bids")],
        [InlineKeyboardButton(text="Создать заявку", callback_data="store_bid")],
        [InlineKeyboardButton(text="Выйти", callback_data="logout")]
    ])
