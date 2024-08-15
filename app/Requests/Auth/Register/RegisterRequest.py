import aiohttp


async def make_request(data):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        form = aiohttp.FormData()
        form.add_field('name', data['name'])
        form.add_field('email', data['email'])
        form.add_field('password', data['password'])
        form.add_field('telegram_id', data['telegram_id'])
        async with session.post('https://crypto-admin-backed.ru/api/telegram/auth/register', data=form) as response:
            status = response.status
            response_json = await response.json()
            return [status, response_json]
