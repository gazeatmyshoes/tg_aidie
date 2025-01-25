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
from .firebase_manager import FirebaseManager

# Настройка логирования
logger = logging.getLogger(__name__)

def error_handler(update, context):
    """Обработчик ошибок"""
    logger.error(f"❌ Update {update} caused error {context.error}")
    if update.effective_message:
        update.effective_message.reply_text(
            "😔 Произошла ошибка при обработке запроса. "
            "Пожалуйста, попробуйте еще раз позже."
        )

def main():
    """Основная функция запуска бота"""
    try:
        logger.info("🔄 Инициализация бота...")
        
        # Инициализация Firebase
        logger.info("🔄 Инициализация Firebase...")
        if not FirebaseManager.init_database():
            logger.error("❌ Ошибка при инициализации Firebase")
            return
        
        # Инициализация бота
        logger.info("🔄 Инициализация Telegram бота...")
        updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        # Регистрация обработчиков
        logger.info("🔄 Регистрация обработчиков команд...")
        dp.add_handler(CommandHandler("start", start_command))
        dp.add_handler(CommandHandler("help", start_command))
        
        # Обработчик callback-запросов от кнопок
        logger.info("🔄 Регистрация обработчика callback-запросов...")
        dp.add_handler(CallbackQueryHandler(handle_callback_query))
        
        # Обработчики сообщений
        logger.info("🔄 Регистрация обработчиков сообщений...")
        dp.add_handler(MessageHandler(Filters.voice, handle_voice))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))
        
        # Обработчик ошибок
        logger.info("🔄 Регистрация обработчика ошибок...")
        dp.add_error_handler(error_handler)

        # Запуск бота
        logger.info("🚀 Бот запущен и готов к работе!")
        updater.start_polling()
        updater.idle()

    except Exception as e:
        logger.error(f"❌ Критическая ошибка при запуске бота: {str(e)}")
        raise

if __name__ == '__main__':
    main()