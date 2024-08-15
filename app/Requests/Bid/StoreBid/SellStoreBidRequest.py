from typing import Optional

import aiohttp


async def make_request(data):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('user_telegram_id', data['user_telegram_id'])
        form.add_field('coin_symbol', data['coin_symbol'])
        form.add_field('currency_symbol', data['currency_symbol'])
        form.add_field('amount', data['amount'])
        form.add_field('price', data['price'])
        form.add_field('type', data['type'])
        form.add_field('payment_method', data['payment_method'])
        form.add_field('number', data['number'])
        async with session.post('https://crypto-admin-backed.ru/api/telegram/bids/store', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
