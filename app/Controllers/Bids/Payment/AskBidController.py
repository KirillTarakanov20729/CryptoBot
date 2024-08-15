from _decimal import Decimal

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Requests.Balance import BalanceRequest
from app.Requests.Bid.Payment import AskBidRequest
from app.Requests.Bid import ShowBidRequest
from app.States.Bid.Payment.AskBidState import AskBidState

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

from app.Keyboards.Bid.Payment.ResponseBidKeyboard import ResponseBidKeyboard

ask_bid_router = Router()


@ask_bid_router.callback_query(F.data == 'ask_bid')
async def ask_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await state.set_state(AskBidState.uuid)
        await callback.answer()
        await callback.message.answer('Введите ID заявки')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@ask_bid_router.message(AskBidState.uuid)
async def ask_bid(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uuid=message.text)
    await state.update_data(user_telegram_id=message.from_user.id)

    if await check_balance(message.from_user.id, message.text):
        data = await state.get_data()

        response = await AskBidRequest.make_request(data)
        status, response_json = response

        if status == 200:
            await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                   text=f"На вашу заявку ответил c ID {response_json['data']['payment']['bid']['uuid']}\n"
                                        f"Данные заявки:\n"
                                        f"{response_json['data']['payment']['bid']['amount']} {response_json['data']['payment']['bid']['coin']['symbol']}\n"
                                        f"{response_json['data']['payment']['bid']['price']} {response_json['data']['payment']['bid']['currency']['symbol']}\n"
                                        f"{response_json['data']['payment']['bid']['type']}\n"
                                        f"ответил {response_json['data']['ask_user']['name']}\n\n"
                                        f"Создан платеж с ID {response_json['data']['payment']['uuid']}",
                                   reply_markup=ResponseBidKeyboard)

            await message.answer("Запрос отправлен. Ждите подтверждения")
        elif status == 403:
            await message.answer(f"Вы не можете ответить на свою заявку")
        elif status == 404:
            await message.answer(f"Заявка уже отвечена другим пользователем")
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
    else:
        await message.answer('Недостаточно криптовалюты на балансе')
        await state.clear()


async def check_balance(user_telegram_id, uuid):
    user_balance_status, user_balance_response = await BalanceRequest.make_request(user_telegram_id)

    show_bid_status, show_bid_response = await ShowBidRequest.make_request(uuid)

    if show_bid_response['data']['type'] == 'buy':
        for coin in range(len(user_balance_response['data'])):
            if user_balance_response['data'][coin]['coin']['symbol'] == show_bid_response['data']['coin']['symbol']:
                if Decimal(user_balance_response['data'][coin]['balance']) >= Decimal(
                        show_bid_response['data']['amount']):
                    return True
                else:
                    return False
    else:
        return True

