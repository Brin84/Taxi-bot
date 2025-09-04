from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime

from keyboards.reply import reply_report_period, reply_drive_menu
from services.google_sheets import get_records_by_day, get_records_by_month

router = Router()


class ReportStates(StatesGroup):
    """FSM для формирования отчёта водителя"""
    choosing_period = State()


@router.message(F.text == "Отчёт 📊")
async def start_report(message: Message, state: FSMContext):
    """Начало выбора периода отчёта"""
    await message.answer(
        "Выберите период отчёта:",
        reply_markup=reply_report_period()
    )
    await state.set_state(ReportStates.choosing_period)


@router.message(ReportStates.choosing_period, F.text.in_(["За день 📆", "За месяц 📅"]))
async def show_report(message: Message, state: FSMContext):
    """Вывод отчёта по выбранному периоду"""
    user_id = message.from_user.id
    today = datetime.now()
    period = "день" if "день" in message.text.lower() else "месяц"

    if period == "день":
        date_str = today.strftime("%d.%m.%Y")
        records = get_records_by_day(user_id, date_str)
    else:
        records = get_records_by_month(user_id, today.month, today.year)

    income = 0
    expense = 0

    for row in records:
        record_type = row[2].strip().lower()
        try:
            amount = float(row[4])
        except:
            continue

        if record_type == "доход":
            income += amount
        elif record_type == "расход":
            expense += amount

    if not records:
        await message.answer(
            f"📊 Отчёт за {period}:\n\nНет данных за выбранный период.",
            reply_markup=reply_drive_menu()
        )
    else:
        balance = income - expense
        await message.answer(
            f"📊 Отчёт за {period}:\n\n"
            f"Доходы: {income:.2f} ₽\n"
            f"Расходы: {expense:.2f} ₽\n"
            f"Баланс: {balance:.2f} ₽",
            reply_markup=reply_drive_menu()
        )

    await state.clear()


@router.message(F.text.in_(["Назад ↩", "🔙 Назад"]))
async def back_to_menu(message: Message, state: FSMContext):
    """Возврат в главное меню водителя"""
    await state.clear()
    await message.answer("Возврат в главное меню", reply_markup=reply_drive_menu())
