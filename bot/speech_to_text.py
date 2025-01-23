from google.cloud import speech_v1p1beta1 as speech
from .config import SPEECH_TO_TEXT_CONFIG, GOOGLE_APPLICATION_CREDENTIALS
import os
import logging
import json

logger = logging.getLogger(__name__)

def transcribe_audio(file_path: str) -> str:
    """
    Преобразование голосового сообщения в текст
    
    Args:
        file_path (str): Путь к аудиофайлу
        
    Returns:
        str: Распознанный текст или сообщение об ошибке
    """
    try:
        logger.info(f"Начало распознавания речи из файла: {file_path}")
        
        # Проверяем наличие файла с учетными данными
        if not os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
            error_msg = f"Google Cloud credentials file not found at {GOOGLE_APPLICATION_CREDENTIALS}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Проверяем наличие аудиофайла
        if not os.path.exists(file_path):
            error_msg = f"Audio file not found at {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Получаем размер файла
        file_size = os.path.getsize(file_path)
        logger.info(f"Размер аудиофайла: {file_size} байт")

        # Создаем клиент
        logger.debug("Создание клиента Speech-to-Text")
        client = speech.SpeechClient()
        
        # Читаем аудиофайл
        logger.debug("Чтение аудиофайла")
        with open(file_path, 'rb') as audio_file:
            content = audio_file.read()

        # Создаем объект аудио
        logger.debug("Создание объекта RecognitionAudio")
        audio = speech.RecognitionAudio(content=content)
        
        # Создаем конфигурацию
        logger.debug("Создание конфигурации распознавания")
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=SPEECH_TO_TEXT_CONFIG['sample_rate_hertz'],
            language_code=SPEECH_TO_TEXT_CONFIG['language_code'],
            enable_automatic_punctuation=True,
            model='default'
        )
        
        # Логируем конфигурацию
        logger.info(f"Конфигурация распознавания: {json.dumps({
            'encoding': 'OGG_OPUS',
            'sample_rate_hertz': SPEECH_TO_TEXT_CONFIG['sample_rate_hertz'],
            'language_code': SPEECH_TO_TEXT_CONFIG['language_code']
        }, ensure_ascii=False)}")

        # Отправляем запрос на распознавание
        logger.info("Отправка запроса на распознавание речи")
        response = client.recognize(config=config, audio=audio)
        
        # Проверяем результаты
        if not response.results:
            logger.warning("Не получено результатов распознавания")
            return "Извините, не удалось распознать речь. Пожалуйста, говорите более четко."
        
        # Получаем результат
        transcript = response.results[0].alternatives[0].transcript
        confidence = response.results[0].alternatives[0].confidence
        
        logger.info(f"Речь успешно распознана (confidence: {confidence:.2f})")
        logger.debug(f"Распознанный текст: {transcript}")
        
        return transcript

    except Exception as e:
        error_msg = f"Ошибка при распознавании речи: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return "Произошла ошибка при распознавании речи. Пожалуйста, попробуйте еще раз."