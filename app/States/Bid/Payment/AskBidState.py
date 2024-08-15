from aiogram.fsm.state import State, StatesGroup


class AskBidState(StatesGroup):
    uuid = State()
    user_telegram_id = State()

