from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    name = State()
    email = State()
    password = State()
    telegram_id = State()