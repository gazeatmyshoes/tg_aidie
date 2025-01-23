import os
import sys
import logging
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
        main_handler = logging.FileHandler('logs/bot.log')
        main_handler.setLevel(logging.INFO)
        main_handler.setFormatter(simple_formatter)
        
        # Файл отладки (все сообщения)
        debug_handler = logging.FileHandler('logs/debug/bot_debug.log')
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
        logger.info("Логирование успешно настроено")
        
    except Exception as e:
        print(f"Ошибка при настройке логирования: {str(e)}")
        raise

def main_with_checks():
    """Запуск бота с проверкой всех необходимых API"""
    logger = logging.getLogger(__name__)
    
    try:
        # Загружаем конфигурацию
        logger.info("🔄 Загрузка конфигурации...")
        config = get_config()
        
        # Проверяем все API
        logger.info("🔄 Проверка API...")
        checker = APIChecker()
        apis_ok, errors = checker.check_all_apis(config)
        
        if not apis_ok:
            error_message = checker.format_error_message(errors)
            logger.error(error_message)
            sys.exit(1)
        
        # Запускаем бота
        logger.info("🚀 Запуск бота...")
        main()

    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    # Настраиваем логирование
    setup_logging()
    
    # Запускаем бота с проверками
    main_with_checks()