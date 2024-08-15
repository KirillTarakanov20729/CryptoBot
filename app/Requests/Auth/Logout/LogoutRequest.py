import aiohttp


async def make_request(telegram_id: int):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('telegram_id', telegram_id)
        async with session.post('https://crypto-admin-backed.ru/api/telegram/auth/logout', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
