from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_income_menu, reply_back_button
from keyboards.reply import reply_drive_menu
from services.google_sheets import add_record


router = Router()

class IncomeStates(StatesGroup):
    """FSM для выбора и добавления дохода"""
    choosing_type = State()
    waiting_amount = State()
    waiting_comment = State()


@router.message(F.text == "Добавить доход 💰")
async def start_income(message: Message, state: FSMContext):
    """Меню добавления дохода"""
    await message.answer(
        "Выберите кнопку для типа дохода🔽",
        reply_markup=reply_income_menu()
    )
    await state.set_state(IncomeStates.choosing_type)


@router.message(IncomeStates.choosing_type, F.text.in_(["Оплата за заказ", "Доплата по заказу"]))
async def ask_income_amount(message: Message, state: FSMContext):
    """Запрос суммы дохода"""
    await state.update_data(income_type=message.text)
    await message.answer("Введите сумму числом: Например (20.00)", reply_markup=reply_back_button())
    await state.set_state(IncomeStates.waiting_amount)


@router.message(IncomeStates.waiting_amount)
async def ask_income_comment(message: Message, state: FSMContext):
    """Запрос комментария"""
    if message.text == "Назад ⬅️":
        await state.set_state(IncomeStates.choosing_type)
        await message.answer("Выберите тип дохода:", reply_markup=reply_income_menu())
        return

    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("❌ Введите корректную сумму или нажмите 'Назад ⬅️'.")
        return

    await state.update_data(amount=amount)
    await message.answer("Добавьте комментарий (например: Гоголя 17)", reply_markup=reply_back_button())
    await state.set_state(IncomeStates.waiting_comment)


@router.message(IncomeStates.waiting_comment)
async def confirm_income(message: Message, state: FSMContext):
    """Подтверждение дохода"""
    user_data = await state.get_data()

    income_type = user_data['income_type']
    amount = user_data['amount']
    comment = message.text

    subcategory = "оплата" if income_type == "Оплата за заказ" else "доплата"

    add_record(
        user_id=message.from_user.id,
        username=message.from_user.full_name,
        record_type='доход',
        subcategory=subcategory,
        amount=amount,
        comment=comment
    )

    await message.answer(
        f"✅ Доход зарегистрирован:\n"
        f"Тип: {income_type}\n"
        f"Сумма: {amount:.2f} бел. руб.\n"
        f"Комментарий: {comment}",
        reply_markup=reply_drive_menu()
    )
    await state.clear()

@router.message(F.text == "Назад ⬅️")
async def back_button(message: Message, state: FSMContext):
    """Возврат в меню дохода"""
    await state.clear()
    await message.answer("Возврат в меню", reply_markup=reply_income_menu())


@router.message(F.text == "🔙 Назад")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    await message.answer("Возврат в главное меню", reply_markup=reply_drive_menu())