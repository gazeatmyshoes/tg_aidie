from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from .handlers import start, button

def main():
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()