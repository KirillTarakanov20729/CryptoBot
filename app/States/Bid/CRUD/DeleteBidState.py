from aiogram.fsm.state import State, StatesGroup


class DeleteBidState(StatesGroup):
    uuid = State()
    user_telegram_id = State()

