from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_admin

router = Router()


@router.message(F.text == "➕ Добавить водителя")
async def add_driver_handler(message: Message):
    """Обработчик кнопки '➕ Добавить водителя' для администраторов"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await message.answer(
        text=(
            "➕ Добавление нового водителя...\n\n"
            "⚠️ Функция пока в разработке."
        )
    )
