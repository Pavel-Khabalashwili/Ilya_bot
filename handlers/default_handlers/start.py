from aiogram.types import Message
from aiogram.filters import Command

from loader import dispatcher


@dispatcher.message(Command("start"))
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
