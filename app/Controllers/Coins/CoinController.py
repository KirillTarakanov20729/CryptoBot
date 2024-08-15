from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.Keyboards.Main.MainInlineKeyboard import MainInlineKeyboard
from app.Requests.Coin import GetCoinsRequest

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

coin_router = Router()


@coin_router.callback_query(F.data == 'coins')
async def get_coins(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        response = await GetCoinsRequest.make_request()
        status, response_json = response

        await callback.answer()
        coins = ""
        for key in range(len(response_json['data'])):
            coins += f'{response_json["data"][key]["name"]} - {response_json["data"][key]["price"]}$\n'

        await callback.message.answer(coins)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")

