from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from loader import dispatcher


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dispatcher.message()
async def echo_command(message: Message):
    await message.answer(f"Я еще не знаком с такой командой: <i>{message.text}</i>\n"
                         f"Список доступных команд: /help", parse_mode=ParseMode.HTML)
