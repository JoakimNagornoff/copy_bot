from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEX_API_URL_PAIRS = os.getenv('DEX_API_URL_PAIRS')
DEX_API_URL_TOKENS = os.getenv('DEX_API_URL_TOKENS')
WALLET_ADDRESSES = eval(os.getenv('WALLET_ADDRESSES'))
CHAT_ID = os.getenv('CHAT_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))