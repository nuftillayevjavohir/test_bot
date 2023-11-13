import json

import aiohttp
from aiogram import types, Router
from aiogram.filters.command import CommandStart

from utils.async_fetch import get, post

router = Router()


@router.message(CommandStart())
async def bot_start(message: types.Message):
    # async with aiohttp.ClientSession() as session:
    #     response = await post(session, 'user-manager/telegram-user/', data={'telegram_id': message.from_user.id})
        # print(response)
    await message.answer(f"Salom, {message.from_user.full_name}!")
