from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_admin

router = Router()


@router.message(F.text == "📤 Экспорт")
async def export_handler(message: Message):
    """Обработчик кнопки '📤 Экспорт' для администраторов"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await message.answer(
        text=(
            "📤 Экспорт данных...\n\n"
            "⚠️ В разработке. Данные будут выгружаться в Google Sheets или Excel."
        )
    )
