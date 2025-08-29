import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_CREDENTIALS_PATH


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

with open(GOOGLE_CREDENTIALS_PATH, 'r') as f:
    creds_dict = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

SPREDSHEET_NAME = 'taxibot'
spreadsheet = client.open(SPREDSHEET_NAME)
sheet = spreadsheet.sheet1


def add_record(record_type: str, subcategory: str, amount: float, comment: str, user_id: int, username: str):
    """Добавление записи в таблицу, согласно полям в таблице"""

    now = datetime.now()
    row = [
        now.strftime('%d.%m.%Y'),
        now.strftime('%H:%M:%S'),
        record_type,
        subcategory,
        amount,
        comment,
        user_id,
        username
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")


def get_records_by_day(user_id: int, date: str):
    """Получение записей по пользователю за день"""
    rows = sheet.get_all_values()[1:]
    filtered = []

    for row in rows:
        row_date = row[0]
        row_user_id = row[6]
        if row_date == date and str(user_id) == row_user_id:
            filtered.append(row)

    return filtered


def get_records_by_month(user_id: int, month: int, year: int):
    """Получение всех записей по user_id за указанный месяц и год"""
    rows = sheet.get_all_values()[1:]
    filtered = []

    for row in rows:
        try:
            row_date = datetime.strptime(row[0], "%d.%m.%Y")
            row_user_id = row[6]
            if row_date.month == month and row_date.year == year and str(user_id) == row_user_id:
                filtered.append(row)
        except (ValueError, IndexError):
            continue

    return filtered


def get_full_report():
    """Получение сводной информации по всем пользователям за весь период"""
    records = sheet.get_all_values()[1:]

    total_income = 0
    total_expense = 0
    user_stats = {}

    for row in records:
        try:
            record_type = row[2].strip().lower()
            amount = float(row[4])
            username = row[7] if len(row) > 7 and row[7] else "Без имени"
        except (IndexError, ValueError):
            continue

        if username not in user_stats:
            user_stats[username] = {"income": 0, "expense": 0}

        if record_type == "доход":
            total_income += amount
            user_stats[username]["income"] += amount
        elif record_type == "расход":
            total_expense += amount
            user_stats[username]["expense"] += amount

    total_diff = total_income - total_expense

    for username, stats in user_stats.items():
        stats["diff"] = stats["income"] - stats["expense"]

    return {
        "total": {
            "income": total_income,
            "expense": total_expense,
            "diff": total_diff
        },
        "users": user_stats
    }


def get_admin_summary(period: str):
    """Получение сводной информации по всем пользователям за указанный период"""
    records = sheet.get_all_values()
    header = records[0]
    rows = records[1:]

    today_str = datetime.now().strftime("%d.%m.%Y")
    month_str = datetime.now().strftime("%m.%Y")

    summary = {}

    for row in rows:
        if len(row) < 8:
            continue

        date, _, record_type, _, amount, _, user_id, username = row

        if period == "day" and date != today_str:
            continue
        if period == "month" and not date.endswith(month_str):
            continue

        try:
            amount = float(amount)
        except ValueError:
            continue

        if username not in summary:
            summary[username] = {"income": 0, "expense": 0}

        if record_type.lower() == "доход":
            summary[username]["income"] += amount
        elif record_type.lower() == "расход":
            summary[username]["expense"] += amount

    lines = []
    total_income = 0
    total_expense = 0

    for user, data in summary.items():
        lines.append(
            f"👤 {user} — Доход: {data['income']:.2f} Byn, Расход: {data['expense']:.2f} Byn"
        )
        total_income += data["income"]
        total_expense += data["expense"]

    lines.append("\n Общий итог:")
    lines.append(f"Доход: {total_income:.2f} Byn")
    lines.append(f"Расход: {total_expense:.2f} Byn")
    lines.append(f"Разница: {total_income - total_expense:.2f} Byn")

    return "\n".join(lines) if lines else "Нет данных за выбранный период."


def get_all_data():
    return sheet.get_all_values()
