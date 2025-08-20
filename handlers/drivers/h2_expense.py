from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.auth import is_driver

router = Router()


class ExpenseStates(StatesGroup):
    """Состояния для добавления расхода"""
    choosing_type = State()
    entering_comment = State()
    entering_amount = State()


@router.message(F.text == "💸 Расход")
async def expense_handler(message: Message, state: FSMContext):
    """Начало ввода расхода — выбор категории"""
    user_id = message.from_user.id
    if not is_driver(user_id):
        await message.answer("❌ Доступ только для водителей.")
        return

    await message.answer(
        text="Выберите категорию расхода:\n\n"
             "⛽ Топливо\n"
             "🔧 Ремонт\n"
             "❔ Другое"
    )
    await state.set_state(ExpenseStates.choosing_type)


@router.message(ExpenseStates.choosing_type)
async def process_expense_type(message: Message, state: FSMContext):
    """Пользователь выбрал категорию — запрашиваем комментарий"""
    expense_type = message.text
    await state.update_data(expense_type=expense_type)

    await message.answer("✏️ Введите комментарий к расходу:")
    await state.set_state(ExpenseStates.entering_comment)


@router.message(ExpenseStates.entering_comment)
async def process_expense_comment(message: Message, state: FSMContext):
    """Пользователь ввел комментарий — запрашиваем сумму"""
    comment = message.text
    await state.update_data(comment=comment)

    await message.answer("💵 Теперь введите сумму расхода (в рублях):")
    await state.set_state(ExpenseStates.entering_amount)


@router.message(ExpenseStates.entering_amount)
async def process_expense_amount(message: Message, state: FSMContext):
    """Получение суммы и комментария — финал"""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("⚠️ Введите сумму числом, например: 15")
        return

    await state.update_data(amount=amount)
    data = await state.get_data()

    await message.answer(
        text=(
            f"✅ Расход добавлен:\n\n"
            f"📂 Категория: {data['expense_type']}\n"
            f"📝 Комментарий: {data['comment']}\n"
            f"💵 Сумма: {data['amount']} руб."
        )
    )

    await state.clear()
