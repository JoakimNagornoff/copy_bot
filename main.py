import asyncio
from telegrambot import main as telegram_main
from solana_dex_monitor import monitor_wallets_and_notify

async def start_services():
    await asyncio.gather(
        telegram_main(),
        monitor_wallets_and_notify(),
    )

if __name__ == '__main__':
    asyncio.run(start_services())
