from aiogram import types, Router

router = Router()


@router.message()
async def bot_echo(message: types.Message):
    await message.answer(message.text)
