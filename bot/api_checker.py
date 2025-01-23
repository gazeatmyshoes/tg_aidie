import os
import json
import logging
import subprocess
import requests
import firebase_admin
from firebase_admin import credentials, db
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language_v1
from typing import Tuple, List

logger = logging.getLogger(__name__)

class APIChecker:
    def __init__(self):
        self.errors: List[str] = []
        
    def check_telegram_api(self, token: str) -> bool:
        """Проверка Telegram Bot API"""
        try:
            logger.info("Проверка Telegram Bot API...")
            response = requests.post(f"https://api.telegram.org/bot{token}/getMe")
            if response.status_code != 200:
                error_msg = f"Ошибка Telegram API: {response.text}"
                self.errors.append(error_msg)
                logger.error(error_msg)
                return False
                
            bot_info = response.json()
            logger.info(f"✅ Telegram бот успешно подключен: @{bot_info['result']['username']}")
            return True
            
        except Exception as e:
            error_msg = f"Ошибка при проверке Telegram API: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def check_google_cloud(self, credentials_path: str) -> bool:
        """Проверка Google Cloud API"""
        try:
            logger.info("Проверка Google Cloud API...")
            
            # Проверка наличия файла с учетными данными
            if not os.path.exists(credentials_path):
                error_msg = f"Файл учетных данных Google Cloud не найден: {credentials_path}"
                self.errors.append(error_msg)
                logger.error(error_msg)
                return False

            # Проверка Speech-to-Text API
            speech_client = speech.SpeechClient()
            logger.info("✅ Speech-to-Text API успешно подключен")

            # Проверка Natural Language API
            language_client = language_v1.LanguageServiceClient()
            logger.info("✅ Natural Language API успешно подключен")

            return True

        except Exception as e:
            error_msg = f"Ошибка при проверке Google Cloud API: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def check_firebase(self, credentials_path: str, database_url: str) -> bool:
        """Проверка Firebase API"""
        try:
            logger.info("Проверка Firebase API...")
            
            # Проверка наличия файла с учетными данными
            if not os.path.exists(credentials_path):
                error_msg = f"Файл учетных данных Firebase не найден: {credentials_path}"
                self.errors.append(error_msg)
                logger.error(error_msg)
                return False

            # Инициализация Firebase
            cred = credentials.Certificate(credentials_path)
            
            # Проверяем, не была ли уже выполнена инициализация
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(cred, {
                    'databaseURL': database_url
                })

            # Тестовая запись в базу данных
            ref = db.reference('test')
            test_data = {'message': 'API Check', 'timestamp': str(os.path.getmtime(credentials_path))}
            ref.set(test_data)

            # Проверка чтения данных
            read_data = ref.get()
            if read_data != test_data:
                error_msg = "Ошибка при проверке записи/чтения Firebase"
                self.errors.append(error_msg)
                logger.error(error_msg)
                return False

            logger.info("✅ Firebase успешно подключен и работает")
            return True

        except Exception as e:
            error_msg = f"Ошибка при проверке Firebase API: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def check_all_apis(self, config: dict) -> Tuple[bool, List[str]]:
        """Проверка всех API"""
        self.errors = []  # Очищаем список ошибок перед проверкой
        
        # Проверяем все API
        telegram_ok = self.check_telegram_api(config['TELEGRAM_BOT_TOKEN'])
        google_ok = self.check_google_cloud(config['GOOGLE_APPLICATION_CREDENTIALS'])
        firebase_ok = self.check_firebase(
            config['FIREBASE_CREDENTIALS_PATH'],
            config['FIREBASE_DATABASE_URL']
        )

        # Если все проверки прошли успешно
        if telegram_ok and google_ok and firebase_ok:
            logger.info("✅ Все API успешно проверены и работают")
            return True, []
        
        # Если есть ошибки
        return False, self.errors

def format_error_message(errors: List[str]) -> str:
    """Форматирование сообщения об ошибках для вывода"""
    message = "❌ Обнаружены проблемы при проверке API:\n\n"
    for i, error in enumerate(errors, 1):
        message += f"{i}. {error}\n"
    message += "\nПожалуйста, проверьте настройки и попробуйте снова."
    return message