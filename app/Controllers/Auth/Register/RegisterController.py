from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.Keyboards.Auth.AuthInlineKeyboard import AuthInlineKeyboard
from app.Requests.Auth.Register import RegisterRequest
from app.States.Auth.Register.RegistrationState import RegistrationState
from app.Keyboards.Main.MainInlineKeyboard import MainInlineKeyboard

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

register_router = Router()


@register_router.callback_query(F.data == 'reg')
async def name(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await callback.answer()
        await callback.message.edit_text('Вы уже авторизованы')
    else:
        await callback.answer()
        await state.set_state(RegistrationState.name)
        await callback.message.edit_text('Введите ваше имя')


@register_router.message(RegistrationState.name)
async def email(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegistrationState.email)
    await message.answer('Введите ваш email')


@register_router.message(RegistrationState.email)
async def password(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(RegistrationState.password)
    await message.answer('Введите ваш пароль')


@register_router.message(RegistrationState.password)
async def register(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    data = await state.get_data()
    response = await RegisterRequest.make_request(data)

    status, response_json = response

    if status == 201:
        await message.answer("Вы успешно зарегистрировались", reply_markup=MainInlineKeyboard)
    elif status == 500:
        await message.answer(f"{response_json['message']}")
    elif status == 422:
        if "errors" in response_json:
            error_messages = ""
            for key in response_json['errors']:
                for error_message in response_json['errors'][key]:
                    error_messages += f'{error_message}\n'

            await message.answer(error_messages, reply_markup=AuthInlineKeyboard)
    else:
        await message.answer('Invalid response')
    await state.clear()
