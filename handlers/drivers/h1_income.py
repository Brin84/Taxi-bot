from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class IncomeStates(StatesGroup):
    """FSM для выбора и добавления дохода"""
    choosing_type = State()
    waiting_comment = State()
    waiting_amount = State()


@router.message(F.text == "Добавить доход 💰")
async def start_income(message: Message, state: FSMContext):
    """Запуск FSM: выбор типа дохода"""
    await message.answer(
        "Выберите тип дохода:",
        reply_markup=None
    )
    await state.set_state(IncomeStates.choosing_type)


@router.message(IncomeStates.choosing_type, F.text.in_(["Оплата за заказ", "Доплата по заказу"]))
async def income_type_chosen(message: Message, state: FSMContext):
    """Обработка выбора типа дохода и запрос комментария"""
    await state.update_data(type=message.text)
    await message.answer("Введите комментарий к доходу:")
    await state.set_state(IncomeStates.waiting_comment)


@router.message(IncomeStates.waiting_comment)
async def income_comment_entered(message: Message, state: FSMContext):
    """Сохраняем комментарий и спрашиваем сумму"""
    await state.update_data(comment=message.text)
    await message.answer("Введите сумму дохода:")
    await state.set_state(IncomeStates.waiting_amount)


@router.message(IncomeStates.waiting_amount)
async def income_amount_entered(message: Message, state: FSMContext):
    """Сохраняем сумму и завершаем FSM"""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
        return

    data = await state.get_data()
    income_type = data.get("type")
    comment = data.get("comment")

    await message.answer(
        f"✅ Доход сохранён!\n\n"
        f"Тип: <b>{income_type}</b>\n"
        f"Комментарий: <i>{comment}</i>\n"
        f"Сумма: <b>{amount:.2f} ₽</b>",
        parse_mode="HTML"
    )

    await state.clear()
