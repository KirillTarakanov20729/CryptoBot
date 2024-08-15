from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.Keyboards.Auth.AuthInlineKeyboard import AuthInlineKeyboard
from app.Requests.Auth.Logout import LogoutRequest

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

logout_router = Router()


@logout_router.callback_query(F.data == 'logout')
async def password(callback: CallbackQuery):
    response = await LogoutRequest.make_request(callback.from_user.id)
    status, response_json = response

    if status == 200:
        await callback.answer()
        await callback.message.answer("Вы вышли из аккаунта", reply_markup=AuthInlineKeyboard)
    elif status == 403:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")

