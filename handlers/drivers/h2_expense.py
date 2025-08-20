from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_back_button, reply_drive_menu
from services.google_sheets import add_expense

router = Router()

class ExpenseStates(StatesGroup):
    """FSM для добавления расхода"""
    choosing_type = State()
    waiting_comment = State()
    waiting_amount = State()


@router.message(F.text == "💸 Расход")
async def start_expense(message: Message, state: FSMContext):
    """Начало добавления расхода"""
    await message.answer(
        "Введите тип расхода:",
        reply_markup=reply_back_button()
    )
    await state.set_state(ExpenseStates.choosing_type)


@router.message(ExpenseStates.choosing_type)
async def expense_type_chosen(message: Message, state: FSMContext):
    """Сохранение типа расхода и запрос комментария"""
    await state.update_data(expense_type=message.text)
    await message.answer("Введите комментарий:", reply_markup=reply_back_button())
    await state.set_state(ExpenseStates.waiting_comment)


@router.message(ExpenseStates.waiting_comment)
async def expense_comment_entered(message: Message, state: FSMContext):
    """Сохранение комментария и запрос суммы"""
    await state.update_data(comment=message.text)
    await message.answer("Введите сумму расхода:")
    await state.set_state(ExpenseStates.waiting_amount)


@router.message(ExpenseStates.waiting_amount)
async def expense_amount_entered(message: Message, state: FSMContext):
    """Получение суммы и сохранение расхода в Google Sheets"""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите сумму числом:")
        return

    data = await state.get_data()
    add_expense(
        driver_id=message.from_user.id,
        expense_type=data["expense_type"],
        comment=data["comment"],
        amount=amount
    )

    await message.answer("Расход успешно добавлен ✅", reply_markup=reply_drive_menu())
    await state.clear()


@router.message(F.text == "Назад ⬅️")
async def back_button(message: Message, state: FSMContext):
    """Возврат в меню водителя"""
    await state.clear()
    await message.answer("Возврат в меню", reply_markup=reply_drive_menu())
