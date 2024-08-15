from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.Keyboards.Main.MainInlineKeyboard import MainInlineKeyboard
from app.Requests.Auth.Login import LoginRequest
from app.States.Auth.Login.LoginState import LoginState

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

login_router = Router()


@login_router.callback_query(F.data == 'login')
async def name(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer("Вы уже авторизованы")
    else:
        await callback.answer()
        await state.set_state(LoginState.email)
        await callback.message.delete()
        await callback.message.answer('Введите ваш email')


@login_router.message(LoginState.email)
async def email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(LoginState.password)
    await message.answer('Введите ваш пароль')


@login_router.message(LoginState.password)
async def password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    data = await state.get_data()
    response = await LoginRequest.make_request(data)

    status, response_json = response

    if status == 200:
        await message.answer("Вы успешно вошли в аккаунт", reply_markup=MainInlineKeyboard)
    elif status == 500:
        await message.answer(f"{response_json['error']}")
    elif status == 401:
        await message.answer(f"{response_json['error']}")
    elif status == 404:
        await message.answer(f"{response_json['error']}")
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
