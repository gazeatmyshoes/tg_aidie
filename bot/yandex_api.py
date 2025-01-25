import json
import requests

def get_sentiment(text, language="ru"):
    """Returns the sentiment of the text using Yandex Natural Language API."""
    url = "https://napi.yandex.net/api/v1/analyze/text/sentiment"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "ApiKey <YANDEX_API_KEY>"
    }
    data = {
        "text": text,
        "language": language
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()