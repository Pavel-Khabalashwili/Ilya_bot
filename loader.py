from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import config

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dispatcher = Dispatcher(storage=storage)
