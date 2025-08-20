import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDS_FILE, SPREADSHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_service():
    """Авторизация и подключение к Google Sheets"""
    creds = Credentials.from_service_account_file(GOOGLE_CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_sheet(sheet_name: str):
    """Получение листа по имени"""
    client = get_service()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    return sheet

def add_income(driver_id: int, income_type: str, comment: str, amount: float):
    """Добавление дохода в таблицу"""
    sheet = get_sheet("Доходы")
    sheet.append_row([str(driver_id), income_type, comment, str(amount)])
    return True

def add_expense(driver_id: int, expense_type: str, comment: str, amount: float):
    """Добавление расхода в таблицу"""
    sheet = get_sheet("Расходы")
    sheet.append_row([str(driver_id), expense_type, comment, str(amount)])
    return True
