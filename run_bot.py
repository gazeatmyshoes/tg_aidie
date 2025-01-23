import os
import sys
import logging
from bot.config import get_config
from bot.api_checker import APIChecker
from bot.main import main

def setup_logging():
    """Настройка логирования"""
    # Создаем директорию для логов, если её нет
    os.makedirs('logs', exist_ok=True)
    
    # Настраиваем формат логирования
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Настраиваем обработчики
    handlers = [
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
    
    # Применяем настройки
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=handlers
    )

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