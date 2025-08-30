import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_CREDENTIALS_PATH

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

with open(GOOGLE_CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
    creds_dict = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

SPREADSHEET_NAME = 'taxibot'
try:
    spreadsheet = client.open(SPREADSHEET_NAME)
    sheet = spreadsheet.sheet1
except Exception as e:
    print(f"❌ Ошибка при открытии таблицы: {e}")
    sheet = None


def add_record(record_type: str, subcategory: str, amount: float, comment: str, user_id: int, username: str):
    """Добавление записи в таблицу"""
    if not sheet:
        print("⚠️ Лист не найден, запись не добавлена")
        return

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
    try:
        sheet.append_row(row, value_input_option="USER_ENTERED")
        print(f"✅ Запись добавлена: {row}")
    except Exception as e:
        print(f"❌ Ошибка при добавлении записи: {e}")


def get_all_records():
    """Возвращает все записи из Google Sheets, кроме заголовка"""
    if not sheet:
        print("⚠️ Лист не найден")
        return []
    try:
        return sheet.get_all_values()[1:]
    except Exception as e:
        print(f"❌ Ошибка при получении всех записей: {e}")
        return []


def get_records_by_day(user_id: int, date: str):
    """Получение записей по пользователю за день"""
    rows = get_all_records()
    filtered = [row for row in rows if row[0] == date and str(row[6]) == str(user_id)]
    return filtered


def get_records_by_month(user_id: int, month: int, year: int):
    """Получение всех записей по user_id за указанный месяц и год"""
    rows = get_all_records()
    filtered = []
    for row in rows:
        try:
            row_date = datetime.strptime(row[0], "%d.%m.%Y")
            if row_date.month == month and row_date.year == year and str(row[6]) == str(user_id):
                filtered.append(row)
        except (ValueError, IndexError):
            continue
    return filtered


def get_admin_summary(period: str):
    """Получение сводной информации по всем пользователям за указанный период"""
    rows = get_all_records()
    today_str = datetime.now().strftime("%d.%m.%Y")
    month_str = datetime.now().strftime("%m.%Y")

    summary = {}
    for row in rows:
        if len(row) < 8:
            continue
        date, _, record_type, _, amount, _, _, username = row

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

    lines.append("\nОбщий итог:")
    lines.append(f"Доход: {total_income:.2f} Byn")
    lines.append(f"Расход: {total_expense:.2f} Byn")
    lines.append(f"Разница: {total_income - total_expense:.2f} Byn")

    return "\n".join(lines) if lines else "Нет данных за выбранный период."
