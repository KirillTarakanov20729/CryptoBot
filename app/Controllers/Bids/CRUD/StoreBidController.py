from _decimal import Decimal

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.Keyboards.Bid.StoreBid.TypesKeyboard import TypesKeyboard
from app.Requests.Bid.StoreBid import BuyStoreBidRequest
from app.Requests.Bid.StoreBid import SellStoreBidRequest
from app.Requests.Balance import BalanceRequest
from app.States.Bid.CRUD.StoreBidState import StoreBidState
from app.Keyboards.Bid.StoreBid.CoinsKeyboard import CoinsKeyboard
from app.Keyboards.Bid.StoreBid.CurrencyKeyboard import CurrencyKeyboard
from app.Keyboards.Bid.StoreBid.PaymentMethodKeyboard import PaymentMethodKeyboard

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

store_bid_router = Router()


@store_bid_router.callback_query(F.data == 'store_bid')
async def store_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await callback.answer()
        await state.set_state(StoreBidState.coin_symbol)
        await callback.message.answer('Выберите криптовалюту', reply_markup=CoinsKeyboard)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@store_bid_router.message(StoreBidState.coin_symbol)
async def store_bid(message: Message, state: FSMContext):
    if message.text not in ["BTC", "ETH", "BNB", "SOL"]:
        await message.answer("Криптовалюты с таким названием не существует")
        await state.clear()
    await state.update_data(coin_symbol=message.text)
    await state.set_state(StoreBidState.amount)
    await message.answer('Укажите количество криптовалюты', reply_markup=ReplyKeyboardRemove())


@store_bid_router.message(StoreBidState.amount)
async def store_bid(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(StoreBidState.currency_symbol)
    await message.answer('Укажите валюту', reply_markup=CurrencyKeyboard)


@store_bid_router.message(StoreBidState.currency_symbol)
async def store_bid(message: Message, state: FSMContext):
    await state.update_data(currency_symbol=message.text)
    await state.set_state(StoreBidState.price)
    await message.answer('Введите сумму', reply_markup=ReplyKeyboardRemove())


@store_bid_router.message(StoreBidState.price)
async def store_bid(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(StoreBidState.type)
    await message.answer('Выберите тип', reply_markup=TypesKeyboard)


@store_bid_router.message(StoreBidState.type)
async def store_bid(message: Message, state: FSMContext):
    if message.text == 'sell':
        data = await state.get_data()
        if await check_balance(message.from_user.id, data['coin_symbol'], data['amount']):
            await state.update_data(type=message.text)
            await state.set_state(StoreBidState.payment_method)
            await message.answer('Выберите способ оплаты', reply_markup=PaymentMethodKeyboard)
        else:
            await message.answer('Недостаточно криптовалюты на балансе')
            await state.clear()

    else:
        await state.update_data(type=message.text)
        await state.set_state(StoreBidState.payment_method)
        await message.answer('Выберите способ оплаты', reply_markup=PaymentMethodKeyboard)


@store_bid_router.message(StoreBidState.payment_method)
async def store_bid(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    await state.update_data(user_telegram_id=message.from_user.id)
    data = await state.get_data()
    if data['type'] == 'buy':
        response = await BuyStoreBidRequest.make_request(data)

        status, response_json = response

        if status == 201:
            await message.answer('Ваша заявка успешно создана')
        elif status == 422:
            if "errors" in response_json:
                error_messages = ""
                for key in response_json['errors']:
                    for error_message in response_json['errors'][key]:
                        error_messages += f'{error_message}\n'

                await message.answer(error_messages)
        await state.clear()
    else:
        await state.set_state(StoreBidState.number)
        await message.answer('Введите номер телефона или номер карты', reply_markup=ReplyKeyboardRemove())


@store_bid_router.message(StoreBidState.number)
async def store_bid(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    response = await SellStoreBidRequest.make_request(data)

    status, response_json = response

    if status == 201:
        await message.answer('Ваша заявка успешно создана', reply_markup=ReplyKeyboardRemove())
    elif status == 422:
        if "errors" in response_json:
            error_messages = ""
            for key in response_json['errors']:
                for error_message in response_json['errors'][key]:
                    error_messages += f'{error_message}\n'

            await message.answer(error_messages, reply_markup=ReplyKeyboardRemove())

    await state.clear()


async def check_balance(user_telegram_id, coin_symbol, amount):
    user_balance_status, user_balance_response = await BalanceRequest.make_request(user_telegram_id)

    for coin in range(len(user_balance_response['data'])):
        if user_balance_response['data'][coin]['coin']['symbol'] == coin_symbol:
            if Decimal(user_balance_response['data'][coin]['balance']) >= Decimal(amount):
                return True
            else:
                return False
