import os
from datetime import datetime

import pandas as pd
from aiogram import Router, F
from aiogram.types import FSInputFile, Message

from keyboards.reply import reply_export_report
from services.google_sheets import get_all_data

router = Router()

EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


@router.message(F.text == "Экспорт данных 📤")
async def export_handler(message: Message):
    """Экспорт всех данных и отправка админу"""
    await message.answer("Данные экспортируются...", reply_markup=reply_export_report())


@router.message(F.text.in_(["📆 За день", "📅 За месяц", "⌚ За всё время"]))
async def export_report_handler(message: Message):
    """Выгрузка данных по выбранному периоду"""
    all_data = get_all_data()
    if not all_data or len(all_data) < 2:
        await message.answer("❌ Данных нет.")
        return

    columns = [col.strip().lower() for col in all_data[0]]
    df = pd.DataFrame(all_data[1:], columns=columns)

    df["дата"] = pd.to_datetime(df["дата"], errors="coerce", dayfirst=True).dt.date

    now = datetime.now()
    period_text = message.text

    if period_text == "📆 За день":
        df = df[df["дата"] == now.date()]
        file_name = f"export_day_{now.strftime('%Y-%m-%d')}.xlsx"
    elif period_text == "📅 За месяц":
        df = df[(df["дата"].apply(lambda d: d.month)) == now.month]
        df = df[df["дата"].apply(lambda d: d.year) == now.year]
        file_name = f"export_month_{now.strftime('%Y-%m')}.xlsx"
    else:
        file_name = f"export_all_{now.strftime('%Y-%m-%d')}.xlsx"

    if df.empty:
        await message.answer("❌ Данных за выбранный период нет.")
        return

    file_path = os.path.join(EXPORT_DIR, file_name)

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Все записи", index=False)
        worksheet = writer.sheets["Все записи"]
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)

        for user, user_df in df.groupby("имя"):
            user_df.to_excel(writer, sheet_name=str(user)[:31], index=False)
            user_ws = writer.sheets[str(user)[:31]]
            for i, col in enumerate(user_df.columns):
                max_len = max(user_df[col].astype(str).map(len).max(), len(col)) + 2
                user_ws.set_column(i, i, max_len)

        summary = (
            df.groupby("имя")["сумма"]
            .apply(lambda x: pd.to_numeric(x, errors="coerce").sum())
            .reset_index()
        )
        summary.rename(columns={"сумма": "Итого"}, inplace=True)
        summary.to_excel(writer, sheet_name="Сводка", index=False)
        summary_ws = writer.sheets["Сводка"]
        for i, col in enumerate(summary.columns):
            max_len = max(summary[col].astype(str).map(len).max(), len(col)) + 2
            summary_ws.set_column(i, i, max_len)

    await message.answer_document(
        FSInputFile(file_path),
        caption=f"Экспорт данных за {period_text}",
    )
