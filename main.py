from copy_bot import setup_bot

if __name__ == '__main__':
    updater = setup_bot()
    updater.start_polling()
    updater.idle()