import pandas as pd
from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from datetime import datetime

from keyboards.reply import reply_export_report
from services.google_sheets import get_all_data

router = Router()


@router.message(F.text == "Экспорт данных 📤")
async def export_handler(message: Message):
    """Экспорт всех данных в CSV и отправка администратору"""
    await message.answer("Данные экспортируются...", reply_markup=reply_export_report())


@router.message(F.text.in_(["📆 За день", "📅 За месяц", "⌚ За всё время"]))
async def export_report_handler(message: Message):
    """Выгрузка из GS по дате"""
    all_data = get_all_data()

    columns = [col.strip().lower() for col in all_data[0]]
    df = pd.DataFrame(all_data[1:], columns=columns)
    print(df.columns)
    now = datetime.now()
    period_text = message.text

    if period_text == "📆 За день":
        df = df[df['дата'] == now.strftime("%d.%m.%Y")]
        file_name = f"export_day_{now.strftime('%Y-%m-%d')}.xlsx"

    elif period_text == "📅 За месяц":
        month_year = now.strftime("%m.%Y")
        df = df[df['дата'].str.endswith(month_year)]
        file_name = f"export_month_{now.strftime('%Y-%m')}.xlsx"

    else:
        file_name = f"export_all_{now.strftime('%Y-%m-%d')}.xlsx"

    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Все записи", index=False)

        for user, user_df in df.groupby("имя"):
            user_df.to_excel(writer, sheet_name=str(user)[:31], index=False)

        summary = (
            df.groupby("имя")["сумма"]
            .apply(lambda x: pd.to_numeric(x, errors='coerce').sum())
            .reset_index()
        )
        summary.rename(columns={"сумма": "Итого"}, inplace=True)
        summary.to_excel(writer, sheet_name="Сводка", index=False)

    await message.answer_document(
        FSInputFile(file_name),
        caption=f"Экспорт данных за {period_text}",
    )