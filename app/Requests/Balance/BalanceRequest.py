import aiohttp


async def make_request(telegram_id: int):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get('https://crypto-admin-backed.ru/api/telegram/balance/show/' + str(telegram_id)) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
