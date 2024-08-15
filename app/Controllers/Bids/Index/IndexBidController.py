from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.Requests.Bid import GetBidsRequest
from app.Keyboards.Bid.BidInlineKeyboard import BidInlineKeyboard
from app.Keyboards.Bid.BidInlineChangePageKeyboard import FirstPageInlineKeyboard
from app.Keyboards.Bid.BidInlineChangePageKeyboard import MidPageInlineKeyboard
from app.Keyboards.Bid.BidInlineChangePageKeyboard import LastPageInlineKeyboard
from app.Middleware.Auth.AuthMiddleware.AuthMiddleware import check_auth

bid_router = Router()

user_page_info = {}


async def process_bids_response(callback: CallbackQuery, response_json: dict):
    if await check_auth(callback.from_user.id):
        await callback.message.delete()
        await callback.message.answer('--------------------')

        for key in range(len(response_json['data'])):
            type_of_order = "Продает" if response_json["data"][key]["type"] == "sell" else "Покупает"
            bid = f'Пользователь {response_json["data"][key]["user"]["name"]}\n' \
                  f'{type_of_order} {response_json["data"][key]["amount"]} {response_json["data"][key]["coin"]["symbol"]} за {response_json["data"][key]["price"]} {response_json["data"][key]["currency"]["symbol"]}\n' \
                  f'{response_json["data"][key]["payment_method"]}\n\n' \
                  f'ID заявки: {response_json["data"][key]["uuid"]}\n\n'

            await callback.answer()
            await callback.message.answer(bid, reply_markup=BidInlineKeyboard)

        user_page_info[callback.from_user.id] = response_json["meta"]["current_page"]

        if response_json["meta"]["current_page"] == 1:
            await callback.message.answer(
                f'{response_json["meta"]["current_page"]} страница из {response_json["meta"]["last_page"]}',
                reply_markup=FirstPageInlineKeyboard)
        elif response_json["meta"]["current_page"] == response_json["meta"]["last_page"]:
            await callback.message.answer(
                f'{response_json["meta"]["current_page"]} страница из {response_json["meta"]["last_page"]}',
                reply_markup=LastPageInlineKeyboard)
        else:
            await callback.message.answer(
                f'{response_json["meta"]["current_page"]} страница из {response_json["meta"]["last_page"]}',
                reply_markup=MidPageInlineKeyboard)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@bid_router.callback_query(F.data == 'bids')
async def get_bids(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        page = user_page_info.get(callback.from_user.id, 1)
        response = await GetBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@bid_router.callback_query(F.data == 'next_page')
async def next_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        page = user_page_info.get(callback.from_user.id, 1)
        page += 1
        response = await GetBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@bid_router.callback_query(F.data == 'previous_page')
async def previous_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        page = user_page_info.get(callback.from_user.id, 1)
        page -= 1
        response = await GetBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@bid_router.callback_query(F.data == 'first_page')
async def first_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        response = await GetBidsRequest.make_request(1, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")


@bid_router.callback_query(F.data == 'last_page')
async def last_page(callback: CallbackQuery):
    if await check_auth(callback.from_user.id):
        page = user_page_info.get(callback.from_user.id, 1)
        response = await GetBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        page = response_json["meta"]["last_page"]
        response = await GetBidsRequest.make_request(page, callback.from_user.id)
        status, response_json = response

        await process_bids_response(callback, response_json)
    else:
        await callback.answer()
        await callback.message.answer("Вы не авторизованы")