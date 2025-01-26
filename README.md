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

4. **Yandex Cloud**
   - Создайте сервисный аккаунт в [Yandex Cloud Console](https://console.cloud.yandex.ru/)
   - Получите API-ключ для сервисного аккаунта
   - Укажите API-ключ и ID каталога:
     ```bash
     YANDEX_API_KEY=ваш_yandex_api_ключ
     YANDEX_FOLDER_ID=ваш_yandex_folder_id
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

5. **Запуск с использованием Docker**
   - Убедитесь, что у вас установлен Docker и Docker Compose
   - Создайте файл `.env` на основе `.env.example` и заполните его необходимыми переменными окружения
   - Запустите контейнеры:
     ```bash
     docker-compose up -d
     ```
   - Остановите контейнеры:
     ```bash
     docker-compose down
     ```

## Использование бота

После запуска бота вы можете использовать следующие команды:

- **/start** - Начать работу с ботом
- **/help** - Получить справку по командам
- **/diary** - Записать новую запись в дневник
- **/mood** - Проанализировать настроение по последним записям

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

## Проверка работоспособности

После запуска бота вы можете проверить его работоспособность, отправив команду `/start`. Бот должен ответить приветственным сообщением. Если бот не отвечает, проверьте логи:

```bash
docker-compose logs -f
```

или, если бот запущен без Docker:

```bash
cat server.log
```

## Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле `LICENSE`.
