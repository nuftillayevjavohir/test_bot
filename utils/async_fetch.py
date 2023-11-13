import hashlib
import json

from data.config_reader import config

BOT_TOKEN = config.bot_token.get_secret_value()
SECRET_KEY = config.secret_key.get_secret_value()

hashed_token = hashlib.sha256((BOT_TOKEN + SECRET_KEY).encode()).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-Telegram-Hashed-Token': hashed_token
}

API_URL = 'http://10.10.2.238:8080/api/'


async def get(session, url, extra_headers=None):
    if extra_headers is dict:
        headers.update(extra_headers)
    async with session.get(API_URL + url, headers=headers) as response:
        response = await response.text()
        return json.loads(response)


async def post(session, url, data, extra_headers=None):
    if extra_headers is dict:
        headers.update(extra_headers)
    async with session.post(API_URL + url, headers=headers, json=data) as response:
        response = await response.text()
        return json.loads(response)
