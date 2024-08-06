from dotenv import load_dotenv
import os

load_dotenv()
def safe_eval(input_str):
    try:
        return eval(input_str, {"__builtins__": None}, {})
    except Exception as e:
        print(f"Error evaluating input: {e}")
        return []

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

WALLET_ADDRESSES = eval(os.getenv('WALLET_ADDRESSES'))
CHAT_ID = os.getenv('CHAT_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))