from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Requests.Bid.Payment import CancelBidRequest
from app.States.Bid.Payment.CancelBidState import CancelBidState
from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth


cancel_bid_router = Router()


@cancel_bid_router.callback_query(F.data == 'cancel_bid')
async def pay_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await state.set_state(CancelBidState.uuid)
        await callback.answer()
        await callback.message.answer('Введите ID платежа')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@cancel_bid_router.message(CancelBidState.uuid)
async def answer(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uuid=message.text)
    await state.update_data(user_telegram_id=message.from_user.id)
    data = await state.get_data()

    cancel_bid_response = await CancelBidRequest.make_request(data)
    status, response_json = cancel_bid_response
    if status == 200:
        if int(response_json['data']['request_user']['telegram_id']) == int(data['user_telegram_id']):
            await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'], text="Пользователь отменил платеж")

            await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'], text="Вы отменили платеж")

        else:
            await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'], text="Пользователь отменил платеж")

            await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'], text="Вы отменили платеж")
    elif status == 403:
        await message.answer(f"Вы не можете отменить чужую заявку")
    elif status == 404:
        await message.answer(f"Заявка имеет неподходящий статус")
    elif status == 500:
        await message.answer(f"Произошла ошибка")
    elif status == 422:
        if "errors" in response_json:
            error_messages = ""
            for key in response_json['errors']:
                for error_message in response_json['errors'][key]:
                    error_messages += f'{error_message}\n'

            await message.answer(error_messages)
    else:
        await message.answer('Invalid response')
    await state.clear()



