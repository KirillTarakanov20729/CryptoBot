from aiogram.fsm.state import State, StatesGroup


class CompleteBidState(StatesGroup):
    uuid = State()

