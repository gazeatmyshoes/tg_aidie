import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Google Cloud configuration
GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/app/keys/google-credentials.json')

# Firebase configuration
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', '/app/keys/firebase-credentials.json')

# Bot settings
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'ru')  # Default language for speech recognition
MAX_AUDIO_DURATION = int(os.getenv('MAX_AUDIO_DURATION', '60'))  # Maximum duration of voice messages in seconds

# API Settings
SPEECH_TO_TEXT_CONFIG = {
    'encoding': 'OGG_OPUS',  # Изменено с LINEAR16 на OGG_OPUS для поддержки голосовых сообщений Telegram
    'sample_rate_hertz': int(os.getenv('SAMPLE_RATE_HERTZ', '16000')),
    'language_code': LANGUAGE_CODE,
}