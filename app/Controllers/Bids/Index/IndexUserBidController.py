from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.Requests.Bid import GetUserBidsRequest
from app.Keyboards.Bid.UserBidInlineDeleteKeyboard import DeleteKeyboard

from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

user_bid_router = Router()

page = 1
last_page = 0


def change_last_page(variable):
    global last_page
    last_page = variable


def change_page(variable):
    global page
    page = variable


async def process_bids_response(callback: CallbackQuery, response_json: dict):
    if await check_auth(callback.from_user.id):
        await callback.message.delete()
        await callback.message.answer('--------------------')

        for key in range(len(response_json['data'])):
            type_of_order = "Продает" if response_json["data"][key]["type"] == "sell" else "Покупает"
            bid = f'Пользователь {response_json["data"][key]["user"]["name"]}\n' \
                  f'{type_of_order} {response_json["data"][key]["amount"]} {response_json["data"][key]["coin"]["symbol"]} за {response_json["data"][key]["price"]}$\n' \
                  f'{response_json["data"][key]["payment_method"]}\n\n' \
                  f'ID заявки: {response_json["data"][key]["uuid"]}\n\n'

            await callback.answer()
            await callback.message.answer(bid, reply_markup=DeleteKeyboard)

        if page == 1:
            await callback.message.answer(
                f'{response_json["meta"]["current_page"]} страница из {response_json["meta"]["last_page"]}')
        elif page == response_json["meta"]["last_page"]:
            await callback.message.answer(
                f'{response_json["meta"]["current_page"]} страница из {response_json["meta"]["last_page"]}')
        else:
            await callback.message.answer(
                f'{response_json["meta"]["current_page"]} страница из {response_json["meta"]["last_page"]}')
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@user_bid_router.callback_query(F.data == 'user_bids')
async def get_bids(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        global page
        response = await GetUserBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response
        change_last_page(response_json["meta"]["last_page"])

        await process_bids_response(callback, response_json)
    else:
        await callback.message.answer("Вы не авторизованы")


@user_bid_router.callback_query(F.data == 'user_next_page')
async def next_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        global page
        page += 1
        response = await GetUserBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@user_bid_router.callback_query(F.data == 'user_previous_page')
async def previous_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        global page
        page -= 1
        response = await GetUserBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@user_bid_router.callback_query(F.data == 'user_first_page')
async def first_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        global page
        page = 1
        response = await GetUserBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@user_bid_router.callback_query(F.data == 'user_last_page')
async def last_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        global page
        global last_page
        change_page(last_page)
        response = await GetUserBidsRequest.make_request(last_page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")