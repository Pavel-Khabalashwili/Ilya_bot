import asyncio

import handlers
from loader import bot, dispatcher
from utils.set_bot_commands import set_default_commands


async def main() -> None:
    await set_default_commands(bot)
    handlers.register_handlers(dispatcher=dispatcher)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
