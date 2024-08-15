from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Requests.Bid import DeleteBidRequest
from app.States.Bid.CRUD.DeleteBidState import DeleteBidState

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

delete_bid_router = Router()


@delete_bid_router.callback_query(F.data == 'delete_bid')
async def delete_bid(callback: CallbackQuery, state: FSMContext):
    if await check_auth(callback.from_user.id):
        await state.set_state(DeleteBidState.uuid)
        await callback.answer()
        await callback.message.answer('Введите ID заявки')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@delete_bid_router.message(DeleteBidState.uuid)
async def delete_bid(message: Message, state: FSMContext):
    await state.update_data(uuid=message.text)
    await state.update_data(user_telegram_id=message.from_user.id)
    data = await state.get_data()

    response = await DeleteBidRequest.make_request(data)

    status, response_json = response

    if status == 200:
        await message.answer("Заявка удалена")
    elif status == 403:
        await message.answer(f"Вы не можете удалить чужую заявку")
    elif status == 500:
        await message.answer(f"Произошла ошибка")
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
