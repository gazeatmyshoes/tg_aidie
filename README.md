# TGAidie - Telegram бот для ведения дневника и анализа настроения

Этот Telegram бот помогает вести дневник и анализировать настроение с использованием Yandex Natural Language API. Поддерживает 5 языков: русский, английский, немецкий, французский и испанский.

## Настройка

Для запуска бота необходимо настроить следующие переменные окружения:

1. **Telegram Bot Token**
   - Создайте бота через [@BotFather](https://t.me/BotFather)
   - Получите токен и добавьте его в `.env` файл:
     ```bash
     TELEGRAM_BOT_TOKEN=ваш_токен_бота
     ```

2. **Google Cloud**
   - Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
   - Скачайте файл с учетными данными (JSON)
   - Укажите путь к файлу и ID проекта:
     ```bash
     GOOGLE_CLOUD_PROJECT_ID=ваш_google_cloud_project_id
     GOOGLE_APPLICATION_CREDENTIALS=путь/к/вашему/google-credentials.json
     ```

3. **Firebase**
   - Создайте проект в [Firebase Console](https://console.firebase.google.com/)
   - Скачайте файл с учетными данными (JSON)
   - Укажите URL базы данных и путь к файлу:
     ```bash
     FIREBASE_DATABASE_URL=ваш_firebase_database_url
     FIREBASE_CREDENTIALS_PATH=путь/к/вашему/firebase-credentials.json
     ```

4. **Запуск бота**
   - Установите зависимости:
     ```bash
     pip install -r requirements.txt
     ```
   - Запустите бота:
     ```bash
     python3 run_bot.py
     ```

## Поддерживаемые языки

Бот поддерживает следующие языки:

- Русский (`ru`)
- Английский (`en`)
- Немецкий (`de`)
- Французский (`fr`)
- Испанский (`es`)

## Разработка

1. Форкните репозиторий
2. Создайте ветку для ваших изменений
3. Сделайте pull request с описанием изменений
4. Убедитесь, что все тесты проходят успешно

## Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле `LICENSE`.
