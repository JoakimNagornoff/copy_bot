import asyncio
import requests
import time
import logging
from config import DEX_API_URL_PAIRS, DEX_API_URL_TOKENS, WALLET_ADDRESSES, CHAT_ID, TELEGRAM_TOKEN, CHECK_INTERVAL
from telegram import Bot

#Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

#logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#last known portfolio for each wallet
last_known_portfolio = {}

async def send_alert(message):
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message)

def fetch_pairs(chain_id, pair_addresses):
    url = f"{DEX_API_URL_PAIRS}/{chain_id}/{pair_addresses}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching pairs data: {str(e)}")
        return None

def fetch_tokens(token_addresses):
    url = f"{DEX_API_URL_TOKENS}/{token_addresses}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"{response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching tokens data: {str(e)}")
        return None

def detect_changes(wallet_address, current_portfolio):
    global last_known_portfolio

    if wallet_address in last_known_portfolio:
        last_portfolio = last_known_portfolio[wallet_address]
        if current_portfolio != last_portfolio:
            return True
    return False

async def monitor_wallets_and_notify():
    global last_known_portfolio
    await send_alert("Monitoring wallets...")
    while True:
        for wallet_address, tag in WALLET_ADDRESSES:
            logger.info(f"Monitoring wallet: {wallet_address} - {tag}")

            pairs_data = fetch_pairs("solana", wallet_address)
            tokens_data = fetch_tokens(wallet_address)
            current_portfolio = {
                "pairs": pairs_data,
                "tokens": tokens_data
            }

            if detect_changes(wallet_address, current_portfolio):
                message = f"New trade detected in {tag} ({wallet_address})!"
                await send_alert(message)
                logger.info(f"Alert sent: {message}")

            last_known_portfolio[wallet_address] = current_portfolio
        
        logger.info(f"Waiting for {CHECK_INTERVAL} seconds...")
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    logger.info("Starting wallet monitoring and notification bot...")
    asyncio.run(monitor_wallets_and_notify())
