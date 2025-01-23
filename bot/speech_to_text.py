from google.cloud import speech_v1p1beta1 as speech
from .config import SPEECH_TO_TEXT_CONFIG, GOOGLE_APPLICATION_CREDENTIALS
import os
import logging

def transcribe_audio(file_path):
    try:
        # Проверяем наличие файла с учетными данными
        if not os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
            raise FileNotFoundError(f"Google Cloud credentials file not found at {GOOGLE_APPLICATION_CREDENTIALS}")

        client = speech.SpeechClient()
        
        # Читаем аудиофайл
        with open(file_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        
        # Используем конфигурацию из config.py
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            **SPEECH_TO_TEXT_CONFIG
        )

        response = client.recognize(config=config, audio=audio)
        
        if not response.results:
            return "Извините, не удалось распознать речь."
            
        return response.results[0].alternatives[0].transcript

    except Exception as e:
        logging.error(f"Error in speech recognition: {str(e)}")
        return "Произошла ошибка при распознавании речи."