from fastapi import FastAPI
from aiogram import types
from bot import dp, bot

from data.config_reader import config

app = FastAPI()
WEBHOOK_PATH = f"/{config.bot_token.get_secret_value()}/"
WEBHOOK_URL = f"https://c8b3-94-141-68-35.ngrok.io{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    print(update)
    telegram_update = types.Update(**update)
    print(telegram_update)
    await dp.feed_update(update=telegram_update, bot=bot)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
