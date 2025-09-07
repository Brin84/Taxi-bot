import os
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

MAIN_ADMIN = int(os.getenv("ADMIN", "0"))

ADMINS_FILE = "config/admins.json"

if not os.path.exists(ADMINS_FILE):
    os.makedirs(os.path.dirname(ADMINS_FILE), exist_ok=True)
    with open(ADMINS_FILE, "w", encoding="utf-8") as f:
        json.dump([MAIN_ADMIN], f, ensure_ascii=False, indent=2)

DRIVERS = [6877046695]

GOOGLE_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_CREDS_PATH",
    "services/creds/taxi_bot_google_sheets.json"
)
