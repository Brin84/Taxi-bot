from aiogram import Router, F
from aiogram.types import FSInputFile, Message

from keyboards.reply import reply_export_report


router = Router()


@router.message(F.text == "Экспорт данных 📤")
async def export_handler(message: Message):
    """Экспорт всех данных в CSV и отправка администратору"""
    await message.answer("Данные экспортируются...", reply_markup=reply_export_report())

