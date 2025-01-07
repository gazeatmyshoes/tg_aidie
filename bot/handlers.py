from telegram import Update
from telegram.ext import CallbackContext
from .speech_to_text import transcribe_audio

def handle_voice(update: Update, context: CallbackContext):
    file = context.bot.get_file(update.message.voice.file_id)
    file.download('voice.ogg')
    text = transcribe_audio('voice.ogg')
    update.message.reply_text(f'Transcribed text: {text}')