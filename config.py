import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

ADMIN = int(os.getenv("ADMIN"))
DRIVERS = [6877046695]
