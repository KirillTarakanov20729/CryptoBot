import aiohttp


async def make_request(page: int, user_telegram_id):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('page', page)
        form.add_field('user_telegram_id', user_telegram_id)
        async with session.post('https://crypto-admin-backed.ru/api/telegram/bids/showUserBids', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
