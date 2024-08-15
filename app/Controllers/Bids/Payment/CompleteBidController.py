from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


from app.States.Bid.Payment.CompleteBidState import CompleteBidState
from app.Requests.Payment import GetPaymentRequest
from app.Requests.Balance import UpdateBalanceRequest
from app.Requests.Bid import DeleteBidRequest
from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth


complete_bid_router = Router()


@complete_bid_router.callback_query(F.data == 'complete_bid')
async def complete_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await state.set_state(CompleteBidState.uuid)
        await callback.answer()
        await callback.message.answer('Введите ID платежа')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@complete_bid_router.message(CompleteBidState.uuid)
async def answer(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(uuid=message.text)
    data = await state.get_data()

    response = await GetPaymentRequest.make_request(data)
    status, response_json = response
    update_data_to_request_user = {}
    update_data_to_response_user = {}

    if response_json['data']['bid']['type'] == 'sell':
        update_data_to_request_user['user_telegram_id'] = response_json['data']['request_user']['telegram_id']
        update_data_to_request_user['amount'] = response_json['data']['bid']['amount']
        update_data_to_request_user['coin_symbol'] = response_json['data']['bid']['coin']['symbol']
        update_data_to_request_user['type'] = 'add'

        update_data_to_response_user['user_telegram_id'] = response_json['data']['response_user']['telegram_id']
        update_data_to_response_user['amount'] = response_json['data']['bid']['amount']
        update_data_to_response_user['coin_symbol'] = response_json['data']['bid']['coin']['symbol']
        update_data_to_response_user['type'] = 'sub'

    if response_json['data']['bid']['type'] == 'buy':
        update_data_to_request_user['user_telegram_id'] = response_json['data']['request_user']['telegram_id']
        update_data_to_request_user['amount'] = response_json['data']['bid']['amount']
        update_data_to_request_user['coin_symbol'] = response_json['data']['bid']['coin']['symbol']
        update_data_to_request_user['type'] = 'sub'

        update_data_to_response_user['user_telegram_id'] = response_json['data']['response_user']['telegram_id']
        update_data_to_response_user['amount'] = response_json['data']['bid']['amount']
        update_data_to_response_user['coin_symbol'] = response_json['data']['bid']['coin']['symbol']
        update_data_to_response_user['type'] = 'add'

    response_request_user = await UpdateBalanceRequest.make_request(update_data_to_request_user)
    response_response_user = await UpdateBalanceRequest.make_request(update_data_to_response_user)

    status_request_user, response_json_request_user = response_request_user
    status_response_user, response_json_response_user = response_response_user

    data_for_delete_bid = {
        'user_telegram_id': response_json['data']['response_user']['telegram_id'],
        'uuid': response_json['data']['bid']['uuid']
    }

    response_delete_bid = await DeleteBidRequest.make_request(data_for_delete_bid)
    status_delete_bid, response_json_delete_bid = response_delete_bid

    if status == 200:
        if status_request_user == 200:
            if status_response_user == 200:
                if status_delete_bid == 200:
                    if response_json['data']['bid']['type'] == 'sell':
                        await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'],
                                               text="Платеж подтвержден. Купленная валюта переведена на ваш баланс")
                        await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                               text="Платеж подтвержден. Проданная валюта переведена с вашего баланса")

                    if response_json['data']['bid']['type'] == 'buy':
                        await bot.send_message(chat_id=response_json['data']['request_user']['telegram_id'],
                                               text="Платеж подтвержден. Проданная валюта переведена с вашего баланса")
                        await bot.send_message(chat_id=response_json['data']['response_user']['telegram_id'],
                                               text="Платеж подтвержден. Купленная валюта переведена на ваш баланс")
                    await state.clear()
                else:
                    await message.answer(f"Ошибка при удалении заявки")
                    await state.clear()
            else:
                await message.answer(f"Ошибка при обновлении баланса")
                await state.clear()
        else:
            await message.answer(f"Ошибка при обновлении баланса")
            await state.clear()
    else:
        await message.answer('Ошибка')
        await state.clear()


