import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import h1_start
from handlers.drivers import h1_income, h2_expense, h3_report
from handlers.admin import h1_summary, h2_export, h3_add_driver, h4_remove_driver, h_back_to_admin_menu, h5_settings

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(h1_start.router)
dp.include_router(h1_income.router)
dp.include_router(h2_expense.router)
dp.include_router(h3_report.router)
dp.include_router(h1_summary.router)
dp.include_router(h2_export.router)
dp.include_router(h3_add_driver.router)
dp.include_router(h4_remove_driver.router)
dp.include_router(h_back_to_admin_menu.router)
dp.include_router(h5_settings.router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
