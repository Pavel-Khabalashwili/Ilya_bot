from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@router.message()
async def echo_command(message: Message):
    await message.answer(
        f"Я еще не знаком с такой командой: <i>{message.text}</i>\n"
        f"Список доступных команд: /help",
        parse_mode=ParseMode.HTML
    )
