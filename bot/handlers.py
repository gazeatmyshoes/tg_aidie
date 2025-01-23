import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from .speech_to_text import transcribe_audio
from .config import MAX_AUDIO_DURATION

def start_command(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("📝 Новая запись", callback_data='new_entry')],
        [InlineKeyboardButton("🎯 Мои цели", callback_data='goals')],
        [InlineKeyboardButton("📊 Анализ настроения", callback_data='mood_analysis')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 Привет! Я AI-Дневник бот.\n\n"
        "Я помогу тебе вести личный дневник и анализировать свои мысли и чувства. "
        "Ты можешь отправлять мне текстовые или голосовые сообщения.\n\n"
        "Выбери действие из меню ниже:"
    )
    
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

def handle_voice(update: Update, context: CallbackContext):
    """Обработчик голосовых сообщений"""
    try:
        # Проверяем длительность аудио
        duration = update.message.voice.duration
        if duration > MAX_AUDIO_DURATION:
            update.message.reply_text(
                f"Извините, но длительность аудио не должна превышать {MAX_AUDIO_DURATION} секунд."
            )
            return

        # Создаем временную директорию для аудио файлов, если её нет
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, f"voice_{update.message.from_user.id}.ogg")

        # Скачиваем файл
        file = context.bot.get_file(update.message.voice.file_id)
        file.download(file_path)

        # Отправляем сообщение о начале обработки
        processing_message = update.message.reply_text(
            "🎯 Обрабатываю ваше голосовое сообщение..."
        )

        # Преобразуем речь в текст
        text = transcribe_audio(file_path)

        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)

        # Обновляем сообщение с результатом
        processing_message.edit_text(
            f"✨ Вот что я распознал:\n\n{text}"
        )

    except Exception as e:
        logging.error(f"Error in voice handler: {str(e)}")
        update.message.reply_text(
            "😔 Извините, произошла ошибка при обработке голосового сообщения. "
            "Пожалуйста, попробуйте еще раз."
        )