import aiohttp
import json
import jwt

from jwt.exceptions import ExpiredSignatureError
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Update

from utils.async_fetch import post, get

from data.config_reader import config


class OwnerCheckMiddleware(BaseMiddleware):
    def __init__(self, redis):
        self.redis = redis
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:

        if event.message:
            print(event.message.text)
            command_split = event.message.text.split(' ', 1)
            if command_split[0] == '/start' and command_split[1].startswith('token'):
                token = "Bearer " + command_split[1][5:]
                async with aiohttp.ClientSession() as session:
                    response = await get(session, 'user-manager/customer/', extra_headers={'Authorization': token})

        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id

        user_data = await self.redis.get(user_id)
        if user_data:
            user_data = json.loads(user_data)
            try:
                jwt.decode(user_data['access'], config.secret_key.get_secret_value(), algorithms=["HS256"])
            except ExpiredSignatureError:
                async with aiohttp.ClientSession() as session:
                    response = await post(session, 'user-manager/token/refresh/',
                                          data={'refresh': user_data['refresh']})
                    new_access = response.get('access', None)
                    if new_access is not None:
                        user_data['access'] = new_access
                        await self.redis.set(user_id, json.dumps(user_data))
                    else:
                        response = await post(session, 'user-manager/telegram-user/', data={'telegram_id': user_id})
                        await self.redis.set(user_id, json.dumps(response))

        elif not user_data:
            async with aiohttp.ClientSession() as session:
                response = await post(session, 'user-manager/telegram-user/', data={'telegram_id': user_id})
                await self.redis.set(user_id, json.dumps(response))
        return await handler(event, data)
