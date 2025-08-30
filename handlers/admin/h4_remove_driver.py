from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import reply_admin_menu
from utils.auth import is_admin
from services.google_sheets import add_record

router = Router()


class RemoveDriverStates(StatesGroup):
    """FSM для удаления водителя"""
    waiting_for_user_id = State()


@router.message(F.text == "Удалить водителя ❌")
async def start_remove_driver(message: Message, state: FSMContext):
    """Начало удаления водителя"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await state.set_state(RemoveDriverStates.waiting_for_user_id)
    await message.answer("Введите Telegram ID водителя, которого нужно удалить:")


@router.message(RemoveDriverStates.waiting_for_user_id)
async def confirm_remove_driver(message: Message, state: FSMContext):
    """Получение ID водителя и фиксация удаления в Google Sheets"""
    try:
        driver_id = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный числовой Telegram ID.")
        return

    add_record(
        user_id=driver_id,
        username="Удалённый водитель",
        record_type="водитель",
        subcategory="удаление",
        amount=0,
        comment="Водитель удалён администратором"
    )

    await message.answer(
        f"✅ Водитель с ID {driver_id} удалён (запись создана в таблице).",
        reply_markup=reply_admin_menu()
    )
    await state.clear()
