from . import custom_handlers
from . import default_handlers

from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    dp.include_router(default_handlers.start.router)
    dp.include_router(default_handlers.help.router)
    dp.include_router(default_handlers.echo.router)
