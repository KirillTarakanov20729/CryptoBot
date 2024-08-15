from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.Requests.Balance import SecretRequest

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

secret_router = Router()


@secret_router.callback_query(F.data == 'secret')
async def get_balance(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        response = await SecretRequest.make_request(telegram_id=callback.from_user.id)
        status, response_json = response

        if status == 200:
            await callback.answer()
            await callback.message.answer('Приятного пользования')

    else:
        await callback.answer()
        await callback.message.answer('Вы не авторизованы')

