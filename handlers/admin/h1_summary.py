from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_admin

router = Router()


@router.message(F.text == "📊 Сводный отчёт")
async def h1_summary_handler(message: Message):
    """Обработчик кнопки '📊 Сводный отчёт' для администраторов"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await message.answer(
        text=(
            "📊 Сводный отчёт:\n\n"
            "👥 Водителей в системе: 0\n"
            "💰 Общие доходы: 0 руб.\n"
            "💸 Общие расходы: 0 руб.\n"
            "📈 Баланс: 0 руб.\n\n"
            "⚠️ Реальные данные будут подтягиваться из Google Sheets."
        )
    )
