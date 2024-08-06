import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, CHAT_ID, WALLET_ADDRESSES

# Initialize the bot
bot = Bot(token=TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Bot started! Monitoring wallets for activity.')

async def send_telegram_message(text: str):
    await bot.send_message(chat_id=CHAT_ID, text=text)

def setup_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    return application

async def main():
    print("Starting telegram bot...")
    application = setup_bot()
    await application.initialize()
    await application.start()
    await send_telegram_message('Bot started! Monitoring wallets for activity.')

    try:
        await application.updater.start_polling()
        await asyncio.Future()
    except Exception as e:
        print(f"Exception in main loop: {e}")
    finally:
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
