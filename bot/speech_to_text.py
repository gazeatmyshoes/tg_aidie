from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(file_path):
    client = speech.SpeechClient()
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code='en-US'
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript