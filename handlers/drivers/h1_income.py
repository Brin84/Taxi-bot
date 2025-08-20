from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_income_menu, reply_back_button
from keyboards.reply import reply_drive_menu
from services.google_sheets import add_income

router = Router()

class IncomeStates(StatesGroup):
    """FSM для выбора и добавления дохода"""
    choosing_type = State()
    waiting_comment = State()
    waiting_amount = State()


@router.message(F.text == "Добавить доход 💰")
async def start_income(message: Message, state: FSMContext):
    """Меню добавления дохода"""
    await message.answer(
        "Выберите тип дохода:",
        reply_markup=reply_income_menu()
    )
    await state.set_state(IncomeStates.choosing_type)


@router.message(IncomeStates.choosing_type, F.text.in_(["Оплата за заказ", "Доплата по заказу"]))
async def income_type_chosen(message: Message, state: FSMContext):
    """Обработка выбора типа дохода и запрос комментария"""
    await state.update_data(income_type=message.text)
    await message.answer("Введите комментарий к доходу:", reply_markup=reply_back_button())
    await state.set_state(IncomeStates.waiting_comment)


@router.message(IncomeStates.waiting_comment)
async def income_comment_entered(message: Message, state: FSMContext):
    """Получение комментария и запрос суммы"""
    await state.update_data(comment=message.text)
    await message.answer("Введите сумму дохода:")
    await state.set_state(IncomeStates.waiting_amount)


@router.message(IncomeStates.waiting_amount)
async def income_amount_entered(message: Message, state: FSMContext):
    """Получение суммы и сохранение дохода в Google Sheets"""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите сумму числом:")
        return

    data = await state.get_data()
    add_income(
        driver_id=message.from_user.id,
        income_type=data["income_type"],
        comment=data["comment"],
        amount=amount
    )

    await message.answer("Доход успешно добавлен ✅", reply_markup=reply_drive_menu())
    await state.clear()


@router.message(F.text == "Назад ⬅️")
async def back_button(message: Message, state: FSMContext):
    """Возврат в главное меню дохода"""
    await state.clear()
    await message.answer("Возврат в меню", reply_markup=reply_income_menu())
