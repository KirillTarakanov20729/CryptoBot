import aiohttp


async def make_request(data):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('uuid', data['uuid'])
        form.add_field('user_telegram_id', data['user_telegram_id'])
        async with session.post('https://crypto-admin-backed.ru/api/telegram/bids/ask', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
