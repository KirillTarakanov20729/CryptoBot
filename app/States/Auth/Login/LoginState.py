from aiogram.fsm.state import State, StatesGroup


class LoginState(StatesGroup):
    email = State()
    password = State()
    telegram_id = State()