from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from app.Keyboards.Main.MainInlineKeyboard import MainInlineKeyboard
from app.Keyboards.Auth.AuthInlineKeyboard import AuthInlineKeyboard


from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth


help_router = Router()


@help_router.message(Command('help'))
async def help_inline(message: Message):
    if await check_auth(message.from_user.id):
        await message.answer("Воспользуйтесь одной из команд", reply_markup=MainInlineKeyboard)
    else:
        await message.answer("Воспользуйтесь одной из команд", reply_markup=AuthInlineKeyboard)


@help_router.message(F.text)
async def help_message(message: Message):
    await message.answer('Я вас не понял, воспользуйтесь командой /help')


