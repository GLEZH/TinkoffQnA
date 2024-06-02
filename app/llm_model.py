import requests
import json
import os
from config import API_KEY

YANDEXGPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
YANDEXGPT_MODEL_URI = "gpt://b1g72uajlds114mlufqi/yandexgpt/latest"


def get_auth_headers():
    if os.getenv('IAM_TOKEN') is not None:
        iam_token = os.environ['IAM_TOKEN']
        headers = {
            'Authorization': f'Bearer {iam_token}',
        }
    elif os.getenv('API_KEY') is not None:
        api_key = API_KEY
        headers = {
            'Authorization': f'Api-Key {api_key}',
        }
    else:
        raise RuntimeError(
            'Please save either an IAM token or an API key into a corresponding IAM_TOKEN or API_KEY environment '
            'variable.')
    return headers


def generate_answer(question, system_prompt, sources):
    # Объединение текстов источников
    context = "\n\n".join([f"{source['title']}\n{source['description']}\n{source['url']}" for source in sources])
    messages = [
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": f"Context: {context}\n\nQuestion: {question}\nAnswer:"}
    ]

    request_body = {
        "modelUri": YANDEXGPT_MODEL_URI,
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": messages
    }

    headers = get_auth_headers()
    response = requests.post(YANDEXGPT_API_URL, headers=headers, data=json.dumps(request_body))

    if response.status_code != 200:
        raise RuntimeError(
            f'Invalid response received: code: {response.status_code}, message: {response.text}'
        )

    response_data = response.json()
    answer = response_data.get("choices", [{}])[0].get("text", "")

    return answer, sources[0]['url']  # Возвращаем URL первого источника как основную ссылку
