import logging
from aiogram.exceptions import (
    TelegramAPIError, TelegramUnauthorizedError,
    TelegramBadRequest, TelegramMethod,
    TelegramForbiddenError, TelegramNetworkError,
    TelegramServerError, RestartingTelegram,
    AiogramError, TelegramConflictError,
    DetailedAiogramError, TelegramNotFound,
    TelegramRetryAfter, TelegramMigrateToChat,
    ClientDecodeError, TelegramEntityTooLarge,
    CallbackAnswerException, UnsupportedKeywordArgument
)
from aiogram import types, F
from aiogram import Router

router = Router()


@router.error(F.update.message.as_("message"))
async def handle_my_custom_exception(event: types.ErrorEvent, message: types.Message):
    logging.critical("Critical error caused by %s", event.exception, exc_info=True)
    return True
    # await message.answer("Oops, something went wrong!")
