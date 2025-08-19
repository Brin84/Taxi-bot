import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from handlers.h1_start import router as start_router
from handlers.admin import *
from handlers.drivers import *
from config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(start_router)
    # dp.include_router(admin_router)
    # dp.include_router(drivers_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
