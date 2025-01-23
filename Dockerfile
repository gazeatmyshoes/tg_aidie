# Используем официальный образ Python
FROM python:3.8-slim

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание необходимых директорий
RUN mkdir -p /app/temp /app/keys /app/logs

# Установка прав на директории
RUN chmod 777 /app/temp /app/keys /app/logs

# Установка переменных окружения по умолчанию
ENV PYTHONUNBUFFERED=1 \
    LANGUAGE_CODE=ru \
    MAX_AUDIO_DURATION=60 \
    SAMPLE_RATE_HERTZ=16000 \
    GOOGLE_APPLICATION_CREDENTIALS=/app/keys/google-credentials.json \
    FIREBASE_CREDENTIALS_PATH=/app/keys/firebase-credentials.json

# Проверка наличия необходимых директорий при запуске
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; assert os.path.exists('/app/temp') and os.path.exists('/app/keys') and os.path.exists('/app/logs')"

# Запуск бота
CMD ["python", "run_bot.py"]