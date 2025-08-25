from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_expense_back, reply_drive_menu
from services.google_sheets import add_record

router = Router()

class ExpenseStates(StatesGroup):
    """FSM для расходов"""
    waiting_for_amount_and_comment = State()


@router.message(F.text == "Добавить расход 🧾")
async def start_expense(message: Message, state: FSMContext):
    """Начало добавления расхода"""
    await message.answer(
        "<b>Укажите расход:</b>\n"
        "Пример:⏬\n"
        "<i>20 топливо</i>\n",
        reply_markup=reply_expense_back(),
        parse_mode="HTML"
    )
    await state.set_state(ExpenseStates.waiting_for_amount_and_comment)


@router.message(ExpenseStates.waiting_for_amount_and_comment)
async def process_expense(message: Message, state: FSMContext):
    """Получение суммы и комментария"""
    if message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Возврат в главное меню", reply_markup=reply_drive_menu())
        return

    try:
        parts = message.text.split(maxsplit=1)
        amount = float(parts[0].replace(",", "."))
        comment = parts[1] if len(parts) > 1 else "-"
    except (ValueError, IndexError):
        await message.answer("❌ Введите корректно, например: 20 заправка")
        return

    add_record(
        user_id=message.from_user.id,
        username=message.from_user.full_name,
        record_type='расход',
        subcategory="расход",
        amount=amount,
        comment=comment
    )

    await message.answer(
        f"✅ Расход зарегистрирован:\n"
        f"Сумма: {amount:.2f} ₽\n"
        f"Комментарий: {comment}",
        reply_markup=reply_drive_menu()
    )
    await state.clear()


@router.message(F.text == "🔙 Назад")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    await message.answer("Возврат в главное меню", reply_markup=reply_drive_menu())
