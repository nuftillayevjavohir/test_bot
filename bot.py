import asyncio
import aioredis

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums.parse_mode import ParseMode

from middlewares.owner_check import OwnerCheckMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from data.config_reader import config

from handlers.errors import error_handler
from handlers.users import start, help, echo


async def on_startup(bot):
    await set_default_commands(bot)
    await on_startup_notify(bot)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_routers(
        error_handler.router,
        start.router,
        help.router,
        echo.router

    )

#
# async def main():
#     try:
#         redis = await aioredis.Redis.from_url(config.redis_url)
#     except Exception as e:
#         print(f"Failed to connect to Redis: {e}")
#         return
#
#     bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
#     dp = Dispatcher(storage=RedisStorage(redis=redis))
#
#     dp.update.middleware(OwnerCheckMiddleware(redis))
#
#     dp.include_routers(
#         error_handler.router,
#         start.router,
#         help.router,
#         echo.router
#
#     )
#
#     dp.startup.register(on_startup)
#
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
