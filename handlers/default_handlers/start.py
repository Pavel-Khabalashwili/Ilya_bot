from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
