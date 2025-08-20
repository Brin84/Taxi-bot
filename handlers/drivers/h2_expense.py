from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_driver

router = Router()

@router.message(F.text == "💸 Расход")
async def h2_expense_handler(message: Message):
    """Реакция на кнопку '💸 Расход' — доступ только для водителей"""
    user_id = message.from_user.id
    if not is_driver(user_id):
        await message.answer("❌ Доступ только для водителей.")
        return

    await message.answer(
        text=""
    )
