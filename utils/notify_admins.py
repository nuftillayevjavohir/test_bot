import logging

from aiogram import Bot

from data.config_reader import config


async def on_startup_notify(bot: Bot):
    try:
        await bot.send_message(config.admin, text="Bot ishga tushdi")

    except Exception as err:
        logging.exception(err)
