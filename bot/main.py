from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from .handlers import handle_voice, start_command
from .config import TELEGRAM_BOT_TOKEN
import logging

def main():
    # Настройка логирования
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Инициализация бота
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))

    # Запуск бота
    updater.start_polling()
    logging.info("Bot started successfully!")
    updater.idle()

if __name__ == '__main__':
    main()