from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import reply_report_period
from utils.auth import is_driver

router = Router()


@router.message(F.text == "📊 Отчёт")
async def report_handler(message: Message, state: FSMContext):
    """Обработчик кнопки '📊 Отчёт' для водителей"""
    await state.clear()
    await message.answer('Отчет за определенный период', reply_markup=reply_report_period())
