import aiohttp


async def make_request(uuid):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('uuid', uuid)
        async with session.post('https://crypto-admin-backed.ru/api/telegram/bids/show', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
