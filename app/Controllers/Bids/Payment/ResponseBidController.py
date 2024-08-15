from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove

from app.States.Bid.Payment.ResponseBidState import ResponseBidState
from app.States.Bid.Payment.SendNumberState import SendNumberState
from app.Requests.Payment import GetPaymentRequest
from app.Requests.Bid.Payment import ResponseBidRequest
from app.Keyboards.Bid.Payment.PayBidKeyboard import PayBidKeyboard
from app.Keyboards.Bid.Payment.AskContactKeyboard import ReplyContactKeyboard

from app.States.Bid.CRUD.UpdateBidState import UpdateBidState

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

response_bid_route = Router()


@response_bid_route.callback_query(F.data == 'response_bid')
async def response_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await state.set_state(ResponseBidState.uuid)
        await callback.answer()
        await callback.message.answer('Введите ID платежа')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@response_bid_route.message(ResponseBidState.uuid)
async def response_bid(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uuid=message.text)
    data = await state.get_data()

    response = await GetPaymentRequest.make_request(data)
    status, response_json = response

    if status == 200:
        if response_json['data']['bid']['type'] == 'sell':
            data_for_response = {
                'uuid': response_json['data']['bid']['uuid'],
                'user_telegram_id': message.from_user.id
            }

            response_response_bid = await ResponseBidRequest.make_request(data_for_response)
            status_response_bid, response_response_bid_json = response_response_bid

            if status_response_bid == 200:
                await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'],
                                       text=f"Переведите {response_json['data']['bid']['price']} "
                                            f"{response_json['data']['bid']['currency']['symbol']}\n"
                                            f"по номеру {response_json['data']['bid']['number']}\n"
                                            f"банк - {response_json['data']['bid']['payment_method']}\n\n"
                                            f"ID платежа: {response_json['data']['uuid']}", reply_markup=PayBidKeyboard)
                await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                       text=f"Покупатель получил данные. Ожидайте оплаты.")
            elif status_response_bid == 404:
                await message.answer("Заявка имеет другой статус")
                await state.clear()
            elif status_response_bid == 403:
                await message.answer("Запрещен доступ")
                await state.clear()
            else:
                await message.answer("Ошибка")
                await state.clear()

        if response_json['data']['bid']['type'] == 'buy':
            await state.set_state(UpdateBidState.number)
            await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'], text="Продавец отправляет номер. Ожидайте сообщения")

            await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'], text=f"Отправьте номер телефона или номер карты\n\n"
                                                                                                      f"ID платежа: {response_json['data']['uuid']}", reply_markup=ReplyContactKeyboard)


@response_bid_route.message(F.contact)
async def send_number(message: Message, state: FSMContext):
    if await check_auth(message.from_user.id):
        await state.set_state(SendNumberState.uuid)
        await state.update_data(number=message.contact.phone_number)
        await message.answer('Введите ID платежа', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Вы не авторизованы")


@response_bid_route.message(SendNumberState.uuid)
async def store_bid(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uuid=message.text)
    data = await state.get_data()

    response = await GetPaymentRequest.make_request(data)
    status, response_json = response

    data_for_response = {
        'uuid': response_json['data']['bid']['uuid'],
        'user_telegram_id': response_json['data']['response_user']['telegram_id']
    }

    response_response_bid = await ResponseBidRequest.make_request(data_for_response)
    status_response_bid, response_response_bid = response_response_bid

    if status == 200:
        if status_response_bid == 200:
            await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                   text=f"Отправьте {response_json['data']['bid']['price']} {response_json['data']['bid']['currency']['symbol']}\n"
                                        f"на номер {data['number']}\n"
                                        f"Банк - {response_json['data']['bid']['payment_method']}\n\n"
                                        f"ID платежа: {response_json['data']['uuid']}", reply_markup=PayBidKeyboard)

            await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'],
                                   text=f"Покупатель получил данные. Ожидайте оплаты.")

        elif status_response_bid == 404:
            await message.answer("Заявка имеет другой статус")
            await state.clear()
        elif status_response_bid == 403:
            await message.answer("Запрещен доступ")
            await state.clear()
        else:
            await message.answer("Ошибка")
            await state.clear()



