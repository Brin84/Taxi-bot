from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import reply_admin_report_menu, reply_admin_menu
from services.google_sheets import get_admin_summary
from utils.auth import is_admin

router = Router()


@router.message(F.text == "Сводка по водителям 📑")
async def h1_summary_handler(message: Message, state: FSMContext):
    """Обработчик кнопки '📊 Сводный отчёт' для администраторов"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await state.clear()
    await message.answer(
        "Выберите период для отчета",
        reply_markup=reply_admin_report_menu()
    )


@router.message(F.text == "📆 Сегодня")
async def admin_summary_today(message: Message):
    """Отчет за сегодня"""
    report = get_admin_summary("day")
    await message.answer(f"отчет за сегодня\n {report}")


@router.message(F.text == "⏪ Назад")
async def admin_summary_back(message: Message, state: FSMContext):
    """Возврат в админ-меню"""
    await state.clear()
    await message.answer('Админ меню', reply_markup=reply_admin_menu())



