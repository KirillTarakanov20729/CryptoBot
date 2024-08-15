from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from app.Keyboards.Auth.AuthInlineKeyboard import AuthInlineKeyboard
from app.Keyboards.Main.MainInlineKeyboard import MainInlineKeyboard
from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

main_router = Router()


@main_router.message(Command('start'))
async def echo(message: Message):
    if await check_auth(message.from_user.id):
        await message.answer("Добро пожаловать в криптокошелек Crypto", reply_markup=MainInlineKeyboard)
    else:
        await message.answer("Добро пожаловать в криптокошелек Crypto", reply_markup=AuthInlineKeyboard)


