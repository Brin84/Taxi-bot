from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_driver

router = Router()


@router.message(F.text == "📊 Отчёт")
async def h3_report_handler(message: Message):
    """Обработчик кнопки '📊 Отчёт' для водителей"""
    user_id = message.from_user.id
    if not is_driver(user_id):
        await message.answer("❌ Доступ только для водителей.")
        return

    await message.answer(
        text=(
            "📊 Ваш отчёт:\n\n"
            "💰 Доходы: 0 руб.\n"
            "💸 Расходы: 0 руб.\n"
            "📈 Баланс: 0 руб.\n\n"
            "⚠️ Подключение к базе данных в разработке."
        )
    )
