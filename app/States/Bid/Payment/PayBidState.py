from aiogram.fsm.state import State, StatesGroup


class PayBidState(StatesGroup):
    uuid = State()

