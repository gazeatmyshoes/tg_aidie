import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_config() -> Dict[str, Any]:
    """Загрузка и проверка конфигурации"""
    # Проверка наличия файла .env
    if not os.path.exists('.env'):
        error_msg = "❌ Файл .env не найден. Пожалуйста, создайте его и добавьте необходимые переменные."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Загрузка переменных окружения
    load_dotenv()
    logger.info("✅ Переменные окружения успешно загружены из .env")

    config = {
        # Telegram Bot configuration
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),

        # Google Cloud configuration
        'GOOGLE_CLOUD_PROJECT_ID': os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
        'GOOGLE_APPLICATION_CREDENTIALS': os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 
                                                  os.path.abspath('keys/google-credentials.json')),

        # Firebase configuration
        'FIREBASE_DATABASE_URL': os.getenv('FIREBASE_DATABASE_URL'),
        'FIREBASE_CREDENTIALS_PATH': os.getenv('FIREBASE_CREDENTIALS_PATH', 
                                             os.path.abspath('keys/firebase-credentials.json')),

        # Bot settings
        'LANGUAGE_CODE': os.getenv('LANGUAGE_CODE', 'ru'),
        'MAX_AUDIO_DURATION': int(os.getenv('MAX_AUDIO_DURATION', '60')),
        'SAMPLE_RATE_HERTZ': int(os.getenv('SAMPLE_RATE_HERTZ', '16000')),
    }

    # Проверка обязательных параметров
    required_params = [
        'TELEGRAM_BOT_TOKEN',
        'GOOGLE_CLOUD_PROJECT_ID',
        'FIREBASE_DATABASE_URL'
    ]

    missing_params = [param for param in required_params if not config[param]]
    
    if missing_params:
        error_msg = (
            "❌ Отсутствуют обязательные параметры конфигурации:\n"
            f"{', '.join(missing_params)}\n"
            "Пожалуйста, проверьте файл .env"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверка путей к файлам учетных данных
    credentials_files = [
        ('Google Cloud', config['GOOGLE_APPLICATION_CREDENTIALS']),
        ('Firebase', config['FIREBASE_CREDENTIALS_PATH'])
    ]

    for service, path in credentials_files:
        if not os.path.exists(path):
            error_msg = f"❌ Не найден файл учетных данных {service}: {path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

    # Добавляем конфигурацию Speech-to-Text
    config['SPEECH_TO_TEXT_CONFIG'] = {
        'encoding': 'OGG_OPUS',
        'sample_rate_hertz': config['SAMPLE_RATE_HERTZ'],
        'language_code': config['LANGUAGE_CODE'],
    }

    logger.info("✅ Конфигурация успешно загружена и проверена")
    return config

# Загружаем конфигурацию при импорте модуля
try:
    config = get_config()
    
    # Экспортируем переменные для обратной совместимости
    TELEGRAM_BOT_TOKEN = config['TELEGRAM_BOT_TOKEN']
    GOOGLE_CLOUD_PROJECT_ID = config['GOOGLE_CLOUD_PROJECT_ID']
    GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']
    FIREBASE_DATABASE_URL = config['FIREBASE_DATABASE_URL']
    FIREBASE_CREDENTIALS_PATH = config['FIREBASE_CREDENTIALS_PATH']
    LANGUAGE_CODE = config['LANGUAGE_CODE']
    MAX_AUDIO_DURATION = config['MAX_AUDIO_DURATION']
    SPEECH_TO_TEXT_CONFIG = config['SPEECH_TO_TEXT_CONFIG']

except Exception as e:
    logger.error(f"❌ Ошибка при загрузке конфигурации: {str(e)}")
    raise