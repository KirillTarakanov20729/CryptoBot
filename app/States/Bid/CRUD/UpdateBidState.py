from aiogram.fsm.state import State, StatesGroup


class UpdateBidState(StatesGroup):
    number = State()
    uuid = State()

