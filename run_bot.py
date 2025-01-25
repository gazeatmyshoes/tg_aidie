import os
import sys
import logging
import signal
from logging.handlers import RotatingFileHandler
from bot.config import get_config
from bot.api_checker import APIChecker
from bot.main import main

def setup_logging():
    """Настройка логирования"""
    try:
        # Создаем директории для логов
        os.makedirs('logs', exist_ok=True)
        os.makedirs('logs/debug', exist_ok=True)

        # Форматтеры для разных уровней логирования
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Основной файл лога (INFO и выше)
        main_handler = RotatingFileHandler(
            'logs/bot.log',
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3
        )
        main_handler.setLevel(logging.INFO)
        main_handler.setFormatter(simple_formatter)

        # Файл отладки (все сообщения)
        debug_handler = RotatingFileHandler(
            'logs/debug/bot_debug.log',
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)

        # Вывод в консоль (INFO и выше)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        # Настройка корневого логгера
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Очищаем существующие обработчики
        root_logger.handlers = []

        # Добавляем обработчики
        root_logger.addHandler(main_handler)
        root_logger.addHandler(debug_handler)
        root_logger.addHandler(console_handler)

        # Настраиваем логгеры сторонних библиотек
        logging.getLogger('telegram').setLevel(logging.INFO)
        logging.getLogger('urllib3').setLevel(logging.INFO)
        logging.getLogger('google').setLevel(logging.INFO)
        logging.getLogger('firebase_admin').setLevel(logging.INFO)

        logger = logging.getLogger(__name__)
        logger.info("✅ Логирование успешно настроено")

    except Exception as e:
        print(f"❌ Ошибка при настройке логирования: {str(e)}")
        raise

def handle_shutdown(signum, frame):
    """Обработка сигналов завершения"""
    logger = logging.getLogger(__name__)
    logger.info("🛑 Получен сигнал завершения. Остановка бота...")
    sys.exit(0)

def main_with_checks():
    """Запуск бота с проверкой всех необходимых API"""
    logger = logging.getLogger(__name__)

    try:
        logger.info("🔄 Загрузка конфигурации...")
        config = get_config()

        # Проверка обязательных переменных окружения
        required_env_vars = [
            'TELEGRAM_BOT_TOKEN',
            'GOOGLE_APPLICATION_CREDENTIALS',
            'FIREBASE_DATABASE_URL'
        ]
        missing_vars = [var for var in required_env_vars if not config.get(var)]
        if missing_vars:
            logger.error(f"❌ Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}")
            sys.exit(1)

        logger.info("🔄 Проверка API...")
        checker = APIChecker()
        apis_ok, errors = checker.check_all_apis(config)

        if not apis_ok:
            error_message = checker.format_error_message(errors)
            logger.error(error_message)
            sys.exit(1)

        logger.info("🚀 Запуск бота...")
        main()

    except Exception as e:
        logger.exception("❌ Критическая ошибка:")  # Логирует полный traceback
        sys.exit(1)

if __name__ == '__main__':
    # Настройка логирования
    setup_logging()

    # Обработка сигналов
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    # Запуск бота с проверками
    main_with_checks()