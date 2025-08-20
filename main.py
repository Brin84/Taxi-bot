import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import h1_start
from handlers.drivers import h1_income

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(h1_start.router)
dp.include_router(h1_income.router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
