import asyncio
from aiogram import Bot, Dispatcher

from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.help import router as help_router

from bot_config import *

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(help_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())