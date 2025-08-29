import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

ADMIN = int(os.getenv("ADMIN"))
DRIVERS = [6877046695]

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDS_PATH", "services/creds/taxi_bot_google_sheets.json")
