from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import random
from google.cloud import language_v1

# Функция для отображения главного меню
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton('Задать вопрос', callback_data='question')],
        [InlineKeyboardButton('Проанализировать настроение', callback_data='sentiment')],
        [InlineKeyboardButton('Цели', callback_data='goals')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Добро пожаловать в AI-Дневник! Выберите действие:', reply_markup=reply_markup)

# Функция для случайного вопроса
def reflect(update: Update, context):
    questions = ['Что тебя сегодня радовало?', 'Как ты себя чувствуешь сегодня?', 'Что нового ты узнал?']
    question = random.choice(questions)
    update.message.reply_text(question)

# Функция для анализа настроений
def sentiment(update: Update, context):
    text = update.message.text
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    update.message.reply_text(f'Тональность: {sentiment.score} (От -1.0 до 1.0)')

# Обработчик для нажатий на кнопки
def button(update: Update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'question':
        reflect(update, context)
    elif query.data == 'sentiment':
        query.edit_message_text(text='Напишите текст для анализа настроения.')
    elif query.data == 'goals':
        keyboard = [
            [InlineKeyboardButton('Добавить цель', callback_data='add_goal')],
            [InlineKeyboardButton('Просмотреть цели', callback_data='view_goals')],
            [InlineKeyboardButton('Завершить цель', callback_data='complete_goal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='Меню целей:', reply_markup=reply_markup)