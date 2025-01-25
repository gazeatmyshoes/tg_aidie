from typing import Dict

TRANSLATIONS = {
    "ru": {
        "welcome": "👋 Привет, {name}!",
        "menu": "Выберите действие:",
        "new_entry": "📝 Новая запись",
        "new_entry_text": "📝 <b>Новая запись в дневник</b>\n\nОтправьте мне текстовое или голосовое сообщение.",
        "goals": "🎯 Мои цели",
        "mood_analysis": "📊 Анализ настроения",
        "voice_processing": "🎯 Обрабатываю ваше голосовое сообщение...",
        "voice_success": "✨ Вот что я распознал:\n\n{text}\n\n{mood_emoji} Запись сохранена в дневник!",
        "error": "😔 Извините, произошла ошибка. Пожалуйста, попробуйте еще раз.",
        "choose_language": "🌐 Выберите язык:",
        "language_changed": "✅ Язык изменен!",
        "back": "« Назад"
    },
    "en": {
        "welcome": "👋 Hello, {name}!",
        "menu": "Choose an action:",
        "new_entry": "📝 New entry",
        "new_entry_text": "📝 <b>New diary entry</b>\n\nSend me a text or voice message.",
        "goals": "🎯 My goals",
        "mood_analysis": "📊 Mood analysis",
        "voice_processing": "🎯 Processing your voice message...",
        "voice_success": "✨ Here's what I recognized:\n\n{text}\n\n{mood_emoji} Entry saved to diary!",
        "error": "😔 Sorry, an error occurred. Please try again.",
        "choose_language": "🌐 Choose language:",
        "language_changed": "✅ Language changed!",
        "back": "« Back"
    },
    "es": {
        "welcome": "👋 ¡Hola, {name}!",
        "menu": "Elige una acción:",
        "new_entry": "📝 Nueva entrada",
        "new_entry_text": "📝 <b>Nueva entrada en el diario</b>\n\nEnviame un mensaje de texto o voz.",
        "goals": "🎯 Mis objetivos",
        "mood_analysis": "📊 Análisis de humor",
        "voice_processing": "🎯 Procesando tu mensaje de voz...",
        "voice_success": "✨ Esto es lo que reconocí:\n\n{text}\n\n{mood_emoji} ¡Entrada guardada en el diario!",
        "error": "😔 Lo siento, ocurrió un error. Por favor, inténtelo de nuevo.",
        "choose_language": "🌐 Elige idioma:",
        "language_changed": "✅ ¡Idioma cambiado!",
        "back": "« Atrás"
    },
    "fr": {
        "welcome": "👋 Bonjour, {name}!",
        "menu": "Choisissez une action:",
        "new_entry": "📝 Nouvelle entrée",
        "new_entry_text": "📝 <b>Nouvelle entrée dans le journal</b>\n\nEnvoyez-moi un message texte ou vocal.",
        "goals": "🎯 Mes objectifs",
        "mood_analysis": "📊 Analyse d'humeur",
        "voice_processing": "🎯 Traitement de votre message vocal...",
        "voice_success": "✨ Voici ce que j'ai reconnu:\n\n{text}\n\n{mood_emoji} Entrée enregistrée dans le journal!",
        "error": "😔 Désolé, une erreur s'est produite. Veuillez réessayer.",
        "choose_language": "🌐 Choisissez la langue:",
        "language_changed": "✅ Langue changée!",
        "back": "« Retour"
    },
    "de": {
        "welcome": "👋 Hallo, {name}!",
        "menu": "Wählen Sie eine Aktion:",
        "new_entry": "📝 Neuer Eintrag",
        "new_entry_text": "📝 <b>Neuer Tagebucheintrag</b>\n\nSenden Sie mir eine Text- oder Sprachnachricht.",
        "goals": "🎯 Meine Ziele",
        "mood_analysis": "📊 Stimmungsanalyse",
        "voice_processing": "🎯 Verarbeite deine Sprachnachricht...",
        "voice_success": "✨ Hier ist, was ich erkannt habe:\n\n{text}\n\n{mood_emoji} Eintrag im Tagebuch gespeichert!",
        "error": "😔 Entschuldigung, ein Fehler ist aufgetreten. Bitte versuche es erneut.",
        "choose_language": "🌐 Sprache wählen:",
        "language_changed": "✅ Sprache geändert!",
        "back": "« Zurück"
    },
    "zh": {
        "welcome": "👋 你好, {name}!",
        "menu": "选择一个操作:",
        "new_entry": "📝 新条目",
        "new_entry_text": "📝 <b>新日记条目</b>\n\n发送给我文本或语音消息。",
        "goals": "🎯 我的目标",
        "mood_analysis": "📊 情绪分析",
        "voice_processing": "🎯 正在处理您的语音消息...",
        "voice_success": "✨ 这是我识别的内容:\n\n{text}\n\n{mood_emoji} 条目已保存到日记中!",
        "error": "😔 抱歉，发生错误。请再试一次。",
        "choose_language": "🌐 选择语言:",
        "language_changed": "✅ 语言已更改!",
        "back": "« 返回"
    }
}

def get_main_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Создает основную клавиатуру бота с учетом языка"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation('new_entry', lang), callback_data='new_entry')],
        [InlineKeyboardButton(get_translation('goals', lang), callback_data='goals')],
        [InlineKeyboardButton(get_translation('mood_analysis', lang), callback_data='mood_analysis')],
        [InlineKeyboardButton("🌐 " + get_translation('language', lang), callback_data='change_language')]
    ])

def get_translation(key: str, lang: str = "ru", **kwargs) -> str:
    """Получение перевода по ключу с учетом языка"""
    return TRANSLATIONS.get(lang, {}).get(key, "").format(**kwargs)

TRANSLATIONS = {
    "ru": {
        "welcome": "👋 Привет, {name}!",
        "new_entry": "📝 Новая запись",
        "goals": "🎯 Мои цели",
        "mood_analysis": "📊 Анализ настроения",
        "voice_processing": "🎯 Обрабатываю ваше голосовое сообщение...",
        "voice_success": "✨ Вот что я распознал:\n\n{text}\n\n{mood_emoji} Запись сохранена в дневник!",
        "error": "😔 Извините, произошла ошибка. Пожалуйста, попробуйте еще раз."
    },
    "en": {
        "welcome": "👋 Hello, {name}!",
        "new_entry": "📝 New entry",
        "goals": "🎯 My goals",
        "mood_analysis": "📊 Mood analysis",
        "voice_processing": "🎯 Processing your voice message...",
        "voice_success": "✨ Here's what I recognized:\n\n{text}\n\n{mood_emoji} Entry saved to diary!",
        "error": "😔 Sorry, an error occurred. Please try again."
    },
    "es": {
        "welcome": "👋 ¡Hola, {name}!",
        "new_entry": "📝 Nueva entrada",
        "goals": "🎯 Mis objetivos",
        "mood_analysis": "📊 Análisis de humor",
        "voice_processing": "🎯 Procesando tu mensaje de voz...",
        "voice_success": "✨ Esto es lo que reconocí:\n\n{text}\n\n{mood_emoji} ¡Entrada guardada en el diario!",
        "error": "😔 Lo siento, ocurrió un error. Por favor, inténtelo de nuevo."
    },
    "fr": {
        "welcome": "👋 Bonjour, {name}!",
        "new_entry": "📝 Nouvelle entrée",
        "goals": "🎯 Mes objectifs",
        "mood_analysis": "📊 Analyse d'humeur",
        "voice_processing": "🎯 Traitement de votre message vocal...",
        "voice_success": "✨ Voici ce que j'ai reconnu:\n\n{text}\n\n{mood_emoji} Entrée enregistrée dans le journal!",
        "error": "😔 Désolé, une erreur s'est produite. Veuillez réessayer."
    },
    "de": {
        "welcome": "👋 Hallo, {name}!",
        "new_entry": "📝 Neuer Eintrag",
        "goals": "🎯 Meine Ziele",
        "mood_analysis": "📊 Stimmungsanalyse",
        "voice_processing": "🎯 Verarbeite deine Sprachnachricht...",
        "voice_success": "✨ Hier ist, was ich erkannt habe:\n\n{text}\n\n{mood_emoji} Eintrag im Tagebuch gespeichert!",
        "error": "😔 Entschuldigung, ein Fehler ist aufgetreten. Bitte versuche es erneut."
    },
    "zh": {
        "welcome": "👋 你好, {name}!",
        "new_entry": "📝 新条目",
        "goals": "🎯 我的目标",
        "mood_analysis": "📊 情绪分析",
        "voice_processing": "🎯 正在处理您的语音消息...",
        "voice_success": "✨ 这是我识别的内容:\n\n{text}\n\n{mood_emoji} 条目已保存到日记中!",
        "error": "😔 抱歉，发生错误。请再试一次。"
    }
}

def get_translation(key: str, lang: str = "ru", **kwargs) -> str:
    return TRANSLATIONS.get(lang, {}).get(key, "").format(**kwargs)