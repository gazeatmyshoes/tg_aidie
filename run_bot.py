import os
from dotenv import load_dotenv
from bot.main import main
import logging

if __name__ == '__main__':
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    try:
        # Загрузка переменных окружения из .env файла
        load_dotenv()

        # Проверка наличия необходимых переменных окружения
        required_env_vars = [
            'TELEGRAM_BOT_TOKEN',
            'GOOGLE_CLOUD_PROJECT_ID',
            'GOOGLE_APPLICATION_CREDENTIALS',
            'FIREBASE_DATABASE_URL',
            'FIREBASE_CREDENTIALS_PATH'
        ]

        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please check your .env file or environment variables."
            )

        # Запуск бота
        logger.info("Starting the bot...")
        main()

    except Exception as e:
        logger.error(f"Failed to start the bot: {str(e)}")
        raise