import aiohttp


async def make_request(update_data_to_request_user):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('coin_symbol', update_data_to_request_user['coin_symbol'])
        form.add_field('user_telegram_id', update_data_to_request_user['user_telegram_id'])
        form.add_field('amount', update_data_to_request_user['amount'])
        form.add_field('type', update_data_to_request_user['type'])
        async with session.put('https://crypto-admin-backed.ru/api/telegram/balance/update', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
