from aiogram.fsm.state import State, StatesGroup


class StoreBidState(StatesGroup):
    user_telegram_id = State()
    coin_symbol = State()
    currency_symbol = State()
    amount = State()
    price = State()
    type = State()
    payment_method = State()
    number = State()