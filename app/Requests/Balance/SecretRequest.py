import aiohttp


async def make_request(telegram_id: int):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('user_telegram_id', str(telegram_id))
        async with session.put('https://crypto-admin-backed.ru/api/telegram/balance/secret', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
