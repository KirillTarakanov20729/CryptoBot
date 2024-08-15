from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.Requests.Balance import BalanceRequest
from app.Requests.Balance import GetPriceCoinsRequest
from decimal import Decimal

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

balance_router = Router()


@balance_router.callback_query(F.data == 'balance')
async def get_balance(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        balance_response = await BalanceRequest.make_request(callback.from_user.id)
        coins_price = await GetPriceCoinsRequest.make_request()
        status_balance, response_json_balance = balance_response
        coins_price_status, response_json_coins_price = coins_price

        if coins_price_status == 200:
            coin_prices = {}
            for coin_data in response_json_coins_price['data']:
                coin_symbol = coin_data['symbol']
                coin_price = coin_data['price']
                coin_prices[coin_symbol] = coin_price

            bnb_price = coin_prices.get("BNB", 0)
            btc_price = coin_prices.get("BTC", 0)
            eth_price = coin_prices.get("ETH", 0)
            sol_price = coin_prices.get("SOL", 0)
        else:
            await callback.answer()
            await callback.message.edit_text("Произошла ошибка при получении цены монет")
            return None

        if status_balance == 200:
            user_balance = {}
            for balance_data in response_json_balance['data']:
                user_balance[balance_data['coin']['symbol']] = balance_data['balance']

            bnb_amount = user_balance.get("BNB", 0)
            btc_amount = user_balance.get("BTC", 0)
            eth_amount = user_balance.get("ETH", 0)
            sol_amount = user_balance.get("SOL", 0)

            bnb_balance = Decimal(bnb_amount) * Decimal(bnb_price)
            btc_balance = Decimal(btc_amount) * Decimal(btc_price)
            eth_balance = Decimal(eth_amount) * Decimal(eth_price)
            sol_balance = Decimal(sol_amount) * Decimal(sol_price)
            overall_balance = bnb_balance + btc_balance + eth_balance + sol_balance

            bnb_balance = round(bnb_balance, 2)
            btc_balance = round(btc_balance, 2)
            eth_balance = round(eth_balance, 2)
            sol_balance = round(sol_balance, 2)
            overall_balance = round(overall_balance, 2)

            await callback.answer()
            await callback.message.answer("----------------------------------------\n"
                                          f"Ваш баланс: {overall_balance}$\n"
                                          "----------------------------------------\n"
                                          f"{bnb_amount} BNB - {bnb_balance}$\n"
                                          f"{btc_amount} BTC - {btc_balance}$\n"
                                          f"{eth_amount} ETH - {eth_balance}$\n"
                                          f"{sol_amount} SOL - {sol_balance}$\n")
        else:
            await callback.answer()
            await callback.message.answer("Произошла ошибка при получении баланса")
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")
