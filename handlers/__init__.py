from aiogram import Dispatcher

from . import custom_handlers
from . import default_handlers


def register_handlers(dispatcher: Dispatcher):
    """
    Регистрирует все обработчики в диспетчере.
    """
    dispatcher.include_router(custom_handlers.reg_name_router)

    dispatcher.include_router(custom_handlers.edit_router)


    dispatcher.include_router(default_handlers.start_router)
    dispatcher.include_router(default_handlers.help_router)
    dispatcher.include_router(default_handlers.echo_router)

