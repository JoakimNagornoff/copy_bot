
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEX_API_URL = os.getenv('DEX_API_URL')
WALLET_ADDRESSES = os.getenv('WALLET_ADDRESSES').split(',')
CHAT_ID = os.getenv('CHAT_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))