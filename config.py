import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
GROUP_LINK = os.getenv("GROUP_LINK")
DB_PATH = "kurash.db"