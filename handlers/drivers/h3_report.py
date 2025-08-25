from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_report_period, reply_drive_menu

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
    period = "день" if "день" in message.text.lower() else "месяц"

    income = 1500.00
    expense = 300.00
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
