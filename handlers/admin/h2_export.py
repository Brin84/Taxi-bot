import csv
import tempfile
from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from utils.auth import is_admin
from services.google_sheets import get_all_records

router = Router()


@router.message(F.text == "Экспорт данных 📤")
async def export_handler(message: Message):
    """Экспорт всех данных в CSV и отправка администратору"""
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Доступ только для администраторов.")
        return

    records = get_all_records()
    if not records:
        await message.answer("Нет данных для экспорта.")
        return

    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        newline="",
        suffix=".csv",
        encoding="utf-8"
    ) as tmpfile:
        writer = csv.writer(tmpfile)
        writer.writerow(["дата", "время", "тип", "подкатегория", "сумма", "комментарий", "Telegram ID", "имя"])
        writer.writerows(records)
        tmpfile_path = tmpfile.name

    await message.answer_document(FSInputFile(tmpfile_path, filename="taxi_data.csv"))
