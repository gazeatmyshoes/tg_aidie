import logging
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, CallbackQueryHandler,
    Filters, ConversationHandler
)
from .handlers import (
    start_command, handle_voice, handle_text_message,
    handle_callback_query
)
from .config import TELEGRAM_BOT_TOKEN

# Настройка логирования
logger = logging.getLogger(__name__)

def error_handler(update, context):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    if update.effective_message:
        update.effective_message.reply_text(
            "😔 Произошла ошибка при обработке запроса. "
            "Пожалуйста, попробуйте еще раз позже."
        )

def main():
    """Основная функция запуска бота"""
    logger.info("Инициализация бота...")
    
    # Инициализация бота
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", start_command))
    
    # Обработчик callback-запросов от кнопок
    dp.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Обработчики сообщений
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))
    
    # Обработчик ошибок
    dp.add_error_handler(error_handler)

    # Запуск бота
    logger.info("Бот запущен и готов к работе!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()