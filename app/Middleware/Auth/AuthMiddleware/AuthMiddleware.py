import string
import requests

import app.Requests.Auth.AuthMiddleware.CheckAuthRequest as CheckAuthRequest


async def check_auth(telegram_id: string):
    response = await CheckAuthRequest.make_request(telegram_id)

    status, response_json = response
    if status == 200:
        return True
    else:
        return False
