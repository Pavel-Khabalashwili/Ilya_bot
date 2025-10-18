from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from loader import dispatcher
from config_data import DEFAULT_COMMANDS


@dispatcher.message(Command("help"))
async def help_command(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    await message.answer("<b>Команды: </b>" + "\n".join(text), parse_mode=ParseMode.HTML)
