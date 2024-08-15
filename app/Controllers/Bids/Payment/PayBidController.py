from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Requests.Payment import GetPaymentRequest
from app.Requests.Bid.Payment import PayBidRequest
from app.Keyboards.Bid.Payment.CompleteBidKeyboard import CompleteBidKeyboard

from app.States.Bid.Payment.PayBidState import PayBidState
from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth


pay_bid_router = Router()


@pay_bid_router.callback_query(F.data == 'pay_bid')
async def pay_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await state.set_state(PayBidState.uuid)
        await callback.answer()
        await callback.message.answer('Введите ID платежа')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@pay_bid_router.message(PayBidState.uuid)
async def answer(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uuid=message.text)
    data = await state.get_data()

    response = await GetPaymentRequest.make_request(data)
    status, response_json = response

    data_for_pay_bid = {
        'uuid': data['uuid'],
        'user_telegram_id': message.from_user.id
    }
    response_pay_bid = await PayBidRequest.make_request(data_for_pay_bid)
    status_pay_bid, response_json_pay_bid = response_pay_bid

    if status == 200:
        if status_pay_bid == 200:
            if response_json['data']['bid']['type'] == 'sell':
                await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'],
                                       text="Ждите ответ продавца")

                await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                       text="Покупатель перевел сумму. Подтвердите платеж",
                                       reply_markup=CompleteBidKeyboard)
                await state.clear()

            if response_json['data']['bid']['type'] == 'buy':
                await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                       text="Ждите ответ продавца")

                await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'],
                                       text="Покупатель перевел сумму. Подтвердите платеж",
                                       reply_markup=CompleteBidKeyboard)
                await state.clear()

        elif status_pay_bid == 404:
            await message.answer("Заявка имеет другой статус")
            await state.clear()
        elif status_pay_bid == 403:
            await message.answer("Доступ запрещен")
            await state.clear()
        else:
            await message.answer("Ошибка")
            await state.clear()
    else:
        await message.answer("Ошибка")
        await state.clear()