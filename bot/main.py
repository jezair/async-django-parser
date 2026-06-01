import asyncio

from aiogram import Bot, Dispatcher

from bot_config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.books import router as books_router


async def main():
    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(books_router)

    await bot.delete_webhook(drop_pending_updates=True)

    print("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())