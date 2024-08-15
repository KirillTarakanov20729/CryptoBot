from aiogram.fsm.state import State, StatesGroup


class CancelBidState(StatesGroup):
    user_telegram_id = State()
    uuid = State()
