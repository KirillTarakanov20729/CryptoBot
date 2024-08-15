from aiogram.fsm.state import State, StatesGroup


class ResponseBidState(StatesGroup):
    uuid = State()

