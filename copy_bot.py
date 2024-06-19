from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
from config import TELEGRAM_TOKEN, CHECK_INTERVAL
from solana_dex_monitor import monitor_wallets_and_notify


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Bot started! Monitoring wallets for activity.')



def setup_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = update.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    job_queue = updater.job_queue
    job_queue.run_repeating(lambda context: monitor_wallets_and_notify(context), interval=CHECK_INTERVAL, first=0)

    return updater


if __name__ == '__main__':
  updater = setup_bot()
  updater.start_polling()
  updater.idle()