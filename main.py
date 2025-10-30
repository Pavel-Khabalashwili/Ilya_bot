import asyncio

import handlers
from database import create_tables
from loader import bot, dispatcher
from utils.set_bot_commands import set_default_commands


async def main() -> None:
    await set_default_commands(bot)
    create_tables()
    handlers.register_handlers(dispatcher=dispatcher)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
