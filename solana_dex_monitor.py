import asyncio
import requests
import logging
from config import WALLET_ADDRESSES, CHAT_ID, TELEGRAM_TOKEN, CHECK_INTERVAL
from telegram import Bot
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  # Import Retry from urllib3


bot = Bot(token=TELEGRAM_TOKEN)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

last_known_portfolio = {}

async def send_alert(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def fetch_portfolio(wallet_address):
    url = f"https://api.dexscreener.com/latest/dex/search?q=/portfolio/{wallet_address}"
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, timeout=30) 
        response.raise_for_status()
        return response.json()
        #portfolio_data = response.json()
        # solana_portfolio = {
        #       pair for pair in portfolio_data.get("pairs", [])
        #       if pair.get("chainId") == "solana"
        #   ]
        #}
        # return solana_portfolio 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching portfolio data: {str(e)}")
        return None

def detect_new_tokens(wallet_address, current_portfolio):
    global last_known_portfolio

    if wallet_address in last_known_portfolio:
        last_portfolio = last_known_portfolio[wallet_address]["pairs"]
        current_tokens = {pair["pairAddress"] for pair in current_portfolio["pairs"]}
        last_tokens = {pair["pairAddress"] for pair in last_portfolio}

        new_tokens = current_tokens - last_tokens
        return new_tokens
    return set()

async def monitor_wallets_and_notify():
    global last_known_portfolio
    await send_alert("Monitoring wallets...")
    while True:
        for wallet_address, tag in WALLET_ADDRESSES:
            logger.info(f"Monitoring wallet: {wallet_address} - {tag}")
     
            portfolio_data = await fetch_portfolio(wallet_address)
            logger.info(f"response: {portfolio_data}")
            if portfolio_data:
                new_tokens = detect_new_tokens(wallet_address, portfolio_data)
                if new_tokens:
                    for token in new_tokens:
                        message = f"New token detected in {tag} ({wallet_address}): {token}"
                        await send_alert(message)
                        logger.info(f"Alert sent: {message}")
                last_known_portfolio[wallet_address] = portfolio_data

        logger.info(f"Waiting for {CHECK_INTERVAL} seconds...")
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    logger.info("Starting wallet monitoring and notification bot...")
    asyncio.run(monitor_wallets_and_notify())
