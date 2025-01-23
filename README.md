# AI-Дневник Бот

AI-Дневник Бот — это Telegram-бот, разработанный для помощи пользователям в ведении личного дневника с использованием искусственного интеллекта. Бот включает в себя функции голосового ввода, автоматических вопросов для рефлексии, анализа настроений, отслеживания целей и рекомендаций на основе психологии. Все действия пользователя доступны через визуальное меню с использованием Inline Keyboard.

## Функции

1. **Голосовой ввод (Speech-to-Text)**
   - Преобразует голосовые сообщения в текст с использованием Google Cloud Speech-to-Text API
   - Поддерживает сообщения длительностью до 60 секунд
   - Автоматическое определение языка

2. **Автоматические вопросы для рефлексии**
   - Отправляет пользователю случайные вопросы для рефлексии
   - Адаптивные вопросы на основе предыдущих ответов

3. **Анализ настроений**
   - Анализирует настроение текста пользователя с использованием Google Cloud Natural Language API
   - Предоставляет визуальную статистику изменения настроения

4. **Постановка и отслеживание целей**
   - Помогает пользователям устанавливать и отслеживать личные цели
   - Хранение целей в Firebase для синхронизации между устройствами

5. **Рекомендации на основе психологии**
   - Предоставляет психологические советы и рекомендации
   - Персонализированные предложения на основе анализа настроения

6. **Визуальное меню с Inline Keyboard**
   - Интуитивно понятный интерфейс с кнопками
   - Быстрый доступ ко всем функциям

## Получение API ключей и токенов

Перед установкой бота необходимо получить все требуемые API ключи и токены. Ниже приведены подробные инструкции для каждого сервиса.

### 1. Telegram Bot Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например, "AI Diary Bot")
   - Введите username бота (должен заканчиваться на "bot", например "ai_diary_bot")
4. После создания бота вы получите токен вида `123456789:ABCdefGHIjklmNOPQrstUVwxyz`
5. Сохраните этот токен для переменной `TELEGRAM_BOT_TOKEN`

Дополнительно рекомендуется:
- Установить аватар бота командой `/setuserpic`
- Добавить описание командой `/setdescription`
- Установить команды через `/setcommands`:
  ```
  start - Начать работу с ботом
  help - Получить справку
  settings - Настройки бота
  ```

### 2. Google Cloud Platform

1. Создайте аккаунт Google Cloud Platform: [console.cloud.google.com](https://console.cloud.google.com/)
2. Создайте новый проект:
   - Перейдите в [Управление проектами](https://console.cloud.google.com/projectcreate)
   - Введите название проекта (например, "AI Diary Bot")
   - Нажмите "Создать"

3. Включите необходимые API:
   - Перейдите в [API и сервисы > Библиотека](https://console.cloud.google.com/apis/library)
   - Найдите и включите:
     * [Cloud Speech-to-Text API](https://console.cloud.google.com/apis/library/speech.googleapis.com)
     * [Cloud Natural Language API](https://console.cloud.google.com/apis/library/language.googleapis.com)

4. Создайте и настройте сервисный аккаунт:

   a) Создание сервисного аккаунта:
   - Перейдите в [API и сервисы > Учетные данные](https://console.cloud.google.com/apis/credentials)
   - Нажмите "Создать учетные данные" > "Сервисный аккаунт"
   - Заполните форму:
     * Название сервисного аккаунта: "ai-diary-bot"
     * ID сервисного аккаунта: оставьте по умолчанию
     * Описание: "Сервисный аккаунт для AI Diary Bot"
   - Нажмите "Создать и продолжить"

   b) Предоставление доступа:
   - На шаге "Предоставить этому сервисному аккаунту доступ к проекту" добавьте следующие роли:
     * "Владелец" (Owner) - для полного доступа
     * "Пользователь Cloud Speech-to-Text" (Cloud Speech-to-Text User)
     * "Пользователь Cloud Natural Language API" (Cloud Natural Language API User)
   - Нажмите "Готово"

   c) Создание ключа:
   - В списке сервисных аккаунтов найдите созданный аккаунт
   - Нажмите на три точки справа (меню действий)
   - Выберите "Управление ключами"
   - Нажмите "Добавить ключ" > "Создать ключ"
   - Выберите формат JSON
   - Нажмите "Создать"
   - Файл автоматически скачается на ваш компьютер (например, `ai-diary-bot-123456789.json`)

   d) Подготовка ключа:
   - Переименуйте скачанный файл в `google-credentials.json`
   - Создайте директорию `keys` в корне проекта:
     ```bash
     mkdir -p keys
     ```
   - Переместите файл в директорию `keys`:
     ```bash
     mv ~/Downloads/google-credentials.json keys/
     ```
   - Проверьте права доступа:
     ```bash
     chmod 600 keys/google-credentials.json
     ```

   e) Настройка переменной окружения:
   
   Для Linux/Mac:
   ```bash
   # Временно (до перезагрузки)
   export GOOGLE_APPLICATION_CREDENTIALS="/полный/путь/к/проекту/keys/google-credentials.json"

   # Постоянно (добавьте в ~/.bashrc или ~/.zshrc)
   echo 'export GOOGLE_APPLICATION_CREDENTIALS="/полный/путь/к/проекту/keys/google-credentials.json"' >> ~/.bashrc
   source ~/.bashrc
   ```

   Для Windows (PowerShell):
   ```powershell
   # Временно (до перезагрузки)
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\полный\путь\к\проекту\keys\google-credentials.json"

   # Постоянно (через системные переменные)
   [Environment]::SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", "C:\полный\путь\к\проекту\keys\google-credentials.json", "User")
   ```

   Для Docker (добавьте в .env файл):
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=/app/keys/google-credentials.json
   ```

   f) Проверка настройки:
   ```bash
   # Для Linux/Mac
   echo $GOOGLE_APPLICATION_CREDENTIALS
   
   # Для Windows PowerShell
   echo $env:GOOGLE_APPLICATION_CREDENTIALS
   
   # Проверка работоспособности
   python -c "
   from google.cloud import speech
   client = speech.SpeechClient()
   print('Подключение к Google Cloud успешно установлено!')
   "
   ```

5. Сохраните дополнительную информацию:
   - ID проекта (для переменной `GOOGLE_CLOUD_PROJECT_ID`):
     * Найдите его в верхней панели консоли Google Cloud
     * Или выполните команду: `gcloud config get-value project`
   - Убедитесь, что все нужные API включены:
     ```bash
     gcloud services list --enabled
     ```
   - Проверьте квоты и лимиты:
     * [Speech-to-Text квоты](https://console.cloud.google.com/apis/api/speech.googleapis.com/quotas)
     * [Natural Language квоты](https://console.cloud.google.com/apis/api/language.googleapis.com/quotas)

### 3. Firebase

1. Перейдите на [console.firebase.google.com](https://console.firebase.google.com/)
2. Создайте новый проект:
   - Выберите тот же ID проекта, что и в Google Cloud
   - Включите Google Analytics (по желанию)

3. Настройте Realtime Database:
   - В меню слева выберите "Realtime Database"
   - Нажмите "Создать базу данных"
   - Выберите регион (например, "eur3 (europe-west)")
   - Начните в тестовом режиме

4. Получите учетные данные:
   - В настройках проекта (⚙️) выберите "Сервисные аккаунты"
   - Нажмите "Создать новый закрытый ключ"
   - Скачайте файл JSON и переименуйте в `firebase-credentials.json`

5. Сохраните:
   - URL базы данных для переменной `FIREBASE_DATABASE_URL`
   - Файл `firebase-credentials.json` поместите в директорию `keys/`

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/gazeatmyshoes/tg_aidie.git
   cd tg_aidie
   ```

2. Создайте и активируйте виртуальное окружение (рекомендуется):
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   # или
   venv\Scripts\activate  # для Windows
   ```

3. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте переменные окружения:
   ```bash
   cp .env.example .env
   ```
   Отредактируйте файл `.env` и добавьте полученные значения:
   ```env
   # Telegram Bot (от @BotFather)
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmNOPQrstUVwxyz

   # Google Cloud
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=/app/keys/google-credentials.json

   # Firebase
   FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.europe-west1.firebasedatabase.app
   FIREBASE_CREDENTIALS_PATH=/app/keys/firebase-credentials.json

   # Дополнительные настройки (можно оставить по умолчанию)
   LANGUAGE_CODE=ru
   MAX_AUDIO_DURATION=60
   SAMPLE_RATE_HERTZ=16000
   ```

5. Создайте директорию для ключей API и скопируйте файлы:
   ```bash
   mkdir -p keys
   cp path/to/downloads/google-credentials.json keys/
   cp path/to/downloads/firebase-credentials.json keys/
   ```

6. Запустите бота:
   ```bash
   python run_bot.py
   ```

### Проверка настройки API

После установки рекомендуется проверить работу каждого API:

1. **Telegram Bot**:
   ```bash
   curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"
   ```
   Должен вернуть информацию о вашем боте.

2. **Google Cloud**:
   ```bash
   # Проверка аутентификации
   gcloud auth activate-service-account --key-file=keys/google-credentials.json
   
   # Проверка доступа к API
   gcloud services list
   ```
   Должны быть видны включенные API.

3. **Firebase**:
   ```python
   import firebase_admin
   from firebase_admin import credentials, db
   
   # Инициализация Firebase
   cred = credentials.Certificate("keys/firebase-credentials.json")
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'your-database-url'
   })
   
   # Тестовая запись
   ref = db.reference('test')
   ref.set({'message': 'Hello, World!'})
   ```
   Должно создать тестовую запись в базе данных.

## Docker установка

### Использование Docker Compose (рекомендуется)

1. Подготовьте необходимые файлы:
   ```bash
   # Создайте директории для ключей и логов
   mkdir -p keys logs temp
   
   # Скопируйте файл с переменными окружения
   cp .env.example .env
   
   # Поместите ваши ключи API в директорию keys/
   cp path/to/your/google-credentials.json keys/
   cp path/to/your/firebase-credentials.json keys/
   ```

2. Отредактируйте файл .env:
   ```bash
   # Откройте файл в редакторе
   nano .env
   
   # Заполните все необходимые переменные окружения
   TELEGRAM_BOT_TOKEN=your_token_here
   GOOGLE_CLOUD_PROJECT_ID=your_project_id
   FIREBASE_DATABASE_URL=your_database_url
   ```

3. Запустите бота через Docker Compose:
   ```bash
   # Запуск в фоновом режиме
   docker-compose up -d
   
   # Просмотр логов
   docker-compose logs -f
   ```

4. Управление ботом:
   ```bash
   # Остановка бота
   docker-compose stop
   
   # Перезапуск бота
   docker-compose restart
   
   # Полная остановка и удаление контейнера
   docker-compose down
   ```

### Использование Docker напрямую

1. Соберите Docker образ:
   ```bash
   docker build -t aidie-bot .
   ```

2. Запустите контейнер:
   ```bash
   docker run -d \
     --name aidie-bot \
     --restart unless-stopped \
     -v $(pwd)/keys:/app/keys:ro \
     -v $(pwd)/logs:/app/logs \
     -v $(pwd)/temp:/app/temp \
     --env-file .env \
     aidie-bot
   ```

3. Управление контейнером:
   ```bash
   # Просмотр логов
   docker logs -f aidie-bot
   
   # Остановка бота
   docker stop aidie-bot
   
   # Перезапуск бота
   docker restart aidie-bot
   
   # Удаление контейнера
   docker rm -f aidie-bot
   ```

### Проверка работоспособности

1. Проверьте статус контейнера:
   ```bash
   docker ps
   # или
   docker-compose ps
   ```

2. Проверьте логи:
   ```bash
   # Через Docker Compose
   docker-compose logs -f
   
   # Или напрямую через Docker
   docker logs -f aidie-bot
   ```

3. Проверьте наличие необходимых директорий:
   ```bash
   ls -la keys/ logs/ temp/
   ```

## Требования

- Python 3.8 или выше
- Зависимости (устанавливаются автоматически):
  - `python-telegram-bot==13.7`
  - `google-cloud-speech==2.21.0`
  - `google-cloud-language==2.11.1`
  - `firebase-admin==6.2.0`
  - `python-dotenv==1.0.0`

## Структура проекта

```
tg_aidie/
├── bot/
│   ├── __init__.py
│   ├── config.py        # Конфигурация и константы
│   ├── handlers.py      # Обработчики команд
│   ├── main.py         # Основной код бота
│   └── speech_to_text.py # Модуль распознавания речи
├── keys/               # Директория для API ключей
├── temp/              # Временные файлы
├── .env              # Конфигурация окружения
├── .env.example      # Пример конфигурации
├── .gitignore       # Игнорируемые файлы
├── Dockerfile       # Конфигурация Docker
├── README.md        # Документация
├── requirements.txt # Зависимости
└── run_bot.py      # Точка входа
```

## Логирование

Бот ведет логи в файл `bot.log` и в консоль. Уровень логирования можно настроить в файле `config.py`.

## Безопасность

- Все конфиденциальные данные хранятся в `.env` файле
- API ключи и учетные данные не включаются в репозиторий
- Временные файлы автоматически удаляются
- Используется безопасное хранение данных в Firebase

## Устранение неполадок

1. **Ошибка при запуске:**
   - Проверьте наличие всех необходимых переменных в `.env`
   - Убедитесь, что файлы с учетными данными находятся в директории `keys/`

2. **Ошибки распознавания речи:**
   - Проверьте подключение к интернету
   - Убедитесь в правильности настройки Google Cloud API

3. **Проблемы с Firebase:**
   - Проверьте права доступа в консоли Firebase
   - Убедитесь в правильности URL базы данных

## Лицензия

Этот проект лицензирован по лицензии MIT.

## Поддержка

При возникновении проблем:
1. Проверьте лог-файл `bot.log`
2. Создайте Issue в репозитории
3. Свяжитесь с разработчиками