import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
from google.cloud import language_v1
from google.api_core.exceptions import InvalidArgument
from .firebase_manager import FirebaseManager
from .speech_to_text import transcribe_audio
from .config import MAX_AUDIO_DURATION

# Настройка логирования
logger = logging.getLogger(__name__)

def get_main_keyboard():
    """Создает основную клавиатуру бота"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Новая запись", callback_data='new_entry')],
        [InlineKeyboardButton("🎯 Мои цели", callback_data='goals')],
        [InlineKeyboardButton("📊 Анализ настроения", callback_data='mood_analysis')]
    ])

def start_command(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} (@{user.username}) запустил бота")
    
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я AI-Дневник бот. Я помогу тебе вести личный дневник и анализировать "
        "свои мысли и чувства. Ты можешь отправлять мне текстовые или голосовые "
        "сообщения.\n\n"
        "🔥 <b>Возможности</b>:\n"
        "• Записи в дневник (текст/голос)\n"
        "• Постановка и отслеживание целей\n"
        "• Анализ настроения\n"
        "• Рекомендации на основе записей\n\n"
        "Выбери действие из меню ниже:"
    )
    
    logger.info(f"Отправка приветственного сообщения пользователю {user.id}")
    update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.HTML
    )

def analyze_text_sentiment(text: str) -> tuple:
    """
    Анализ настроения текста с помощью Google Natural Language API

    Args:
        text (str): Текст для анализа

    Returns:
        tuple: (sentiment_score, sentiment_magnitude)
    """
    try:
        logger.info("Начало анализа настроения текста")
        logger.debug(f"Исходный текст: {text[:100]}...")

        client = language_v1.LanguageServiceClient()
        
        # Сначала пытаемся анализировать на русском
        try:
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language='ru'
            )
            sentiment = client.analyze_sentiment(
                request={'document': document}
            ).document_sentiment
            return sentiment.score, sentiment.magnitude
        except InvalidArgument:
            # Если русский не поддерживается, переводим на английский
            from google.cloud import translate_v2 as translate
            translate_client = translate.Client()
            translation = translate_client.translate(
                text,
                target_language='en',
                source_language='ru'
            )
            translated_text = translation['translatedText']
            
            document = language_v1.Document(
                content=translated_text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language='en'
            )
            sentiment = client.analyze_sentiment(
                request={'document': document}
            ).document_sentiment
            return sentiment.score, sentiment.magnitude

    except Exception as e:
        logger.error(f"Ошибка при анализе настроения: {str(e)}", exc_info=True)
        return 0, 0
    """
    Анализ настроения текста с помощью Google Natural Language API
    
    Args:
        text (str): Текст для анализа
        
    Returns:
        tuple: (sentiment_score, sentiment_magnitude)
    """
    try:
        logger.info("Начало анализа настроения текста")
        logger.debug(f"Исходный текст: {text[:100]}...")
        
        # Используем Cloud Translation API вместо googletrans
        from google.cloud import translate_v2 as translate
        translate_client = translate.Client()
        
        # Переводим текст на английский
        logger.info("Перевод текста на английский")
        translation = translate_client.translate(
            text,
            target_language='en',
            source_language='ru'
        )
        
        translated_text = translation['translatedText']
        logger.debug(f"Переведенный текст: {translated_text[:100]}...")
        
        # Анализируем настроение переведенного текста
        logger.info("Анализ настроения переведенного текста")
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(
            content=translated_text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language='en'
        )
        
        sentiment = client.analyze_sentiment(
            request={'document': document}
        ).document_sentiment
        
        logger.info(f"Результаты анализа: score={sentiment.score:.2f}, magnitude={sentiment.magnitude:.2f}")
        return sentiment.score, sentiment.magnitude
        
    except Exception as e:
        logger.error(f"Ошибка при анализе настроения: {str(e)}", exc_info=True)
        return 0, 0

def get_mood_emoji(score: float) -> str:
    """Возвращает эмодзи в зависимости от оценки настроения"""
    if score >= 0.5:
        return "😊"
    elif score >= 0.1:
        return "🙂"
    elif score > -0.1:
        return "😐"
    elif score > -0.5:
        return "😕"
    else:
        return "😢"

def save_diary_entry(user_id: int, text: str, sentiment_score: float, 
                    sentiment_magnitude: float) -> bool:
    """Сохранение записи в дневник"""
    return FirebaseManager.save_diary_entry(
        user_id, text, sentiment_score, sentiment_magnitude
    )

def handle_text_message(update: Update, context: CallbackContext):
    """Обработчик текстовых сообщений"""
    user = update.effective_user
    text = update.message.text
    logger.info(f"Получено текстовое сообщение от пользователя {user.id}: {text[:50]}...")

    try:
        # Проверяем, ожидаем ли мы новую цель от пользователя
        if context.user_data.get('waiting_for_goal'):
            logger.info(f"Добавление новой цели для пользователя {user.id}")
            if FirebaseManager.add_goal(user.id, text):
                response = "✅ Цель успешно добавлена!"
            else:
                response = "❌ Произошла ошибка при добавлении цели."
            
            # Сбрасываем флаг ожидания цели
            context.user_data['waiting_for_goal'] = False
            
            # Показываем обновленный список целей
            goals = FirebaseManager.get_goals(user.id)
            if goals:
                response += "\n\n🎯 <b>Ваши текущие цели</b>:\n\n"
                for i, goal in enumerate(goals, 1):
                    status = "✅" if goal.get('completed') else "🔲"
                    response += f"{status} {i}. {goal['text']}\n"
            
            update.message.reply_text(
                response,
                parse_mode=ParseMode.HTML,
                reply_markup=get_main_keyboard()
            )
            return

        # Обычная обработка текстового сообщения
        score, magnitude = analyze_text_sentiment(text)
        mood_emoji = get_mood_emoji(score)
        
        # Сохраняем запись
        if save_diary_entry(user.id, text, score, magnitude):
            response = (
                f"{mood_emoji} Запись сохранена в дневник!\n\n"
                f"📊 Анализ настроения:\n"
                f"• Оценка: {score:.2f}\n"
                f"• Интенсивность: {magnitude:.2f}\n\n"
                "Хотите продолжить?"
            )
        else:
            response = "❌ Произошла ошибка при сохранении записи."
        
        logger.info(f"Отправка ответа пользователю {user.id}")
        update.message.reply_text(response, reply_markup=get_main_keyboard())
        
    except Exception as e:
        logger.error(f"Ошибка при обработке текстового сообщения: {str(e)}")
        update.message.reply_text(
            "😔 Извините, произошла ошибка при обработке сообщения. "
            "Пожалуйста, попробуйте еще раз.",
            reply_markup=get_main_keyboard()
        )

def handle_callback_query(update: Update, context: CallbackContext):
    """Обработчик callback-запросов от кнопок"""
    query = update.callback_query
    user = query.from_user
    logger.info(f"Получен callback-запрос от пользователя {user.id}: {query.data}")

    try:
        # Отправляем уведомление о получении запроса
        query.answer()

        if query.data == 'new_entry':
            text = (
                "📝 <b>Новая запись в дневник</b>\n\n"
                "Отправьте мне текстовое или голосовое сообщение, "
                "и я сохраню его в ваш дневник с анализом настроения."
            )
            query.edit_message_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("« Назад", callback_data='back_to_menu')
                ]])
            )

        elif query.data == 'goals':
            goals = get_user_goals(user.id)
            if goals:
                text = "🎯 <b>Ваши текущие цели</b>:\n\n"
                for i, goal in enumerate(goals, 1):
                    status = "✅" if goal.get('completed') else "🔲"
                    text += f"{status} {i}. {goal['text']}\n"
            else:
                text = "У вас пока нет установленных целей."
            
            keyboard = [
                [InlineKeyboardButton("➕ Добавить цель", callback_data='add_goal')],
                [InlineKeyboardButton("« Назад", callback_data='back_to_menu')]
            ]
            query.edit_message_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif query.data == 'mood_analysis':
            mood_stats = analyze_user_mood_history(user.id)
            if mood_stats:
                text = (
                    "📊 <b>Анализ настроения</b>\n\n"
                    f"За последнюю неделю:\n"
                    f"• Средняя оценка: {mood_stats['avg_score']:.2f}\n"
                    f"• Преобладающее настроение: {mood_stats['dominant_mood']}\n"
                    f"• Количество записей: {mood_stats['entries_count']}\n\n"
                    f"Рекомендация: {mood_stats['recommendation']}"
                )
            else:
                text = (
                    "📊 <b>Анализ настроения</b>\n\n"
                    "У вас пока недостаточно записей для анализа. "
                    "Продолжайте вести дневник, чтобы получить персональную аналитику."
                )

            query.edit_message_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("« Назад", callback_data='back_to_menu')
                ]])
            )

        elif query.data == 'back_to_menu':
            text = (
                "Выберите действие из меню ниже:"
            )
            query.edit_message_text(
                text,
                reply_markup=get_main_keyboard()
            )

        elif query.data == 'add_goal':
            context.user_data['waiting_for_goal'] = True
            text = (
                "🎯 <b>Добавление новой цели</b>\n\n"
                "Отправьте текстовое сообщение с описанием вашей цели."
            )
            query.edit_message_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("« Отмена", callback_data='back_to_menu')
                ]])
            )

    except Exception as e:
        logger.error(f"Ошибка при обработке callback-запроса от {user.id}: {str(e)}")
        try:
            query.edit_message_text(
                "😔 Произошла ошибка. Пожалуйста, попробуйте еще раз.",
                reply_markup=get_main_keyboard()
            )
        except Exception:
            pass

def get_user_goals(user_id: int) -> list:
    """Получение списка целей пользователя"""
    return FirebaseManager.get_goals(user_id)

def analyze_user_mood_history(user_id: int) -> dict:
    """Анализ истории настроения пользователя"""
    entries = FirebaseManager.get_mood_history(user_id)
    if not entries:
        return None

    scores = [entry['sentiment_score'] for entry in entries]
    avg_score = sum(scores) / len(scores)
    
    # Определяем преобладающее настроение
    if avg_score >= 0.5:
        dominant_mood = "Очень позитивное 😊"
        recommendation = "Отличная работа! Продолжайте делиться позитивом!"
    elif avg_score >= 0.1:
        dominant_mood = "Позитивное 🙂"
        recommendation = "Хорошее настроение! Запишите, что помогает вам оставаться позитивным."
    elif avg_score > -0.1:
        dominant_mood = "Нейтральное 😐"
        recommendation = "Попробуйте обратить внимание на приятные моменты дня."
    elif avg_score > -0.5:
        dominant_mood = "Негативное 😕"
        recommendation = "Запишите, что вас беспокоит. Это поможет лучше понять свои эмоции."
    else:
        dominant_mood = "Очень негативное 😢"
        recommendation = "Рекомендуем поговорить с близкими или обратиться к специалисту."

    return {
        'avg_score': avg_score,
        'dominant_mood': dominant_mood,
        'entries_count': len(entries),
        'recommendation': recommendation
    }

def handle_voice(update: Update, context: CallbackContext):
    """Обработчик голосовых сообщений"""
    user = update.effective_user
    logger.info(f"Получено голосовое сообщение от пользователя {user.id}")

    try:
        # Проверяем длительность аудио
        duration = update.message.voice.duration
        if duration > MAX_AUDIO_DURATION:
            logger.warning(f"Слишком длинное голосовое сообщение от пользователя {user.id}: {duration}с")
            update.message.reply_text(
                f"⚠️ Длительность аудио не должна превышать {MAX_AUDIO_DURATION} секунд.",
                reply_markup=get_main_keyboard()
            )
            return

        # Создаем временную директорию для аудио файлов
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, f"voice_{user.id}_{int(datetime.now().timestamp())}.ogg")

        # Скачиваем файл
        logger.info(f"Скачивание голосового сообщения пользователя {user.id}")
        file = context.bot.get_file(update.message.voice.file_id)
        file.download(file_path)

        # Отправляем сообщение о начале обработки
        processing_message = update.message.reply_text(
            "🎯 Обрабатываю ваше голосовое сообщение..."
        )

        # Преобразуем речь в текст
        logger.info(f"Преобразование речи в текст для пользователя {user.id}")
        text = transcribe_audio(file_path)

        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)

        if not text:
            logger.warning(f"Не удалось распознать речь пользователя {user.id}")
            processing_message.edit_text(
                "😔 Извините, не удалось распознать речь. Пожалуйста, попробуйте еще раз.",
                reply_markup=get_main_keyboard()
            )
            return

        # Анализируем настроение
        logger.info(f"Анализ настроения для пользователя {user.id}")
        score, magnitude = analyze_text_sentiment(text)
        mood_emoji = get_mood_emoji(score)

        # Сохраняем запись
        if save_diary_entry(user.id, text, score, magnitude):
            response = (
                f"✨ Вот что я распознал:\n\n"
                f"{text}\n\n"
                f"{mood_emoji} Запись сохранена в дневник!\n\n"
                f"📊 Анализ настроения:\n"
                f"• Оценка: {score:.2f}\n"
                f"• Интенсивность: {magnitude:.2f}"
            )
        else:
            response = (
                f"✨ Вот что я распознал:\n\n"
                f"{text}\n\n"
                "❌ Произошла ошибка при сохранении записи."
            )

        # Обновляем сообщение с результатом
        logger.info(f"Отправка результата пользователю {user.id}")
        processing_message.edit_text(response, reply_markup=get_main_keyboard())

    except Exception as e:
        logger.error(f"Ошибка при обработке голосового сообщения от {user.id}: {str(e)}")
        if 'processing_message' in locals():
            processing_message.edit_text(
                "😔 Извините, произошла ошибка при обработке голосового сообщения. "
                "Пожалуйста, попробуйте еще раз.",
                reply_markup=get_main_keyboard()
            )
        else:
            update.message.reply_text(
                "😔 Извините, произошла ошибка при обработке голосового сообщения. "
                "Пожалуйста, попробуйте еще раз.",
                reply_markup=get_main_keyboard()
            )