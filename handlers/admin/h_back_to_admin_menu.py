from aiogram import Router, F
from aiogram.types import Message
from utils.auth import is_admin
from keyboards.reply import reply_admin_menu

router = Router()


@router.message(F.text == "↩️ В меню")
async def back_to_admin_menu_handler(message: Message):
    """Обработчик кнопки '↩️ В меню' для администраторов"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    await message.answer(
        text="↩️ Вы вернулись в меню администратора.",
        reply_markup=reply_admin_menu()
    )
