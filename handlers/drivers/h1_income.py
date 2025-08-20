from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_income_menu, reply_back_button

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


@router.message(F.text == "Назад ⬅️")
async def back_button(message: Message, state: FSMContext):
    """Возврат в главное меню дохода"""
    await state.clear()
    await message.answer("Возврат в меню ", reply_markup=reply_income_menu())
