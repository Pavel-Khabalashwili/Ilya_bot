from aiogram import Bot
from aiogram.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


async def set_default_commands(bot: Bot):
    commands = []
    for command, description in DEFAULT_COMMANDS:
        commands.append(BotCommand(command=command, description=description))

    await bot.set_my_commands(commands)