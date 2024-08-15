from aiogram.fsm.state import State, StatesGroup


class SendNumberState(StatesGroup):
    number = State()
    uuid = State()

