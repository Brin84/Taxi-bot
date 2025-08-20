from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_admin

router = Router()


@router.message(F.text == "➖ Удалить водителя")
async def remove_driver_handler(message: Message):
    """Обработчик кнопки '➖ Удалить водителя' для администраторов"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await message.answer(
        text=(
            "➖ Удаление водителя...\n\n"
            "⚠️ Функция пока в разработке."
        )
    )
