from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import requests
from app.vector_store import VectorStore
from app.database import init_db, SessionLocal, Document
from config import API_KEY
import os

app = FastAPI()
vector_store = VectorStore()


class Query(BaseModel):
    query: str


class Response(BaseModel):
    text: str
    links: list[str]


@app.on_event("startup")
def on_startup():
    init_db()
    load_dataset()


def load_dataset():
    with open('data/dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)["data"]
    for doc in dataset:
        vector_store.add_to_index(doc["title"], doc["description"], doc["url"])


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
            'Please save either an IAM token or an API key into a corresponding IAM_TOKEN or API_KEY environment variable.')
    return headers


def create_dynamic_prompt(user_query, relevant_docs):
    context = "\n\n".join([f"{doc.title}\n{doc.description}\n{doc.url}" for doc in relevant_docs])
    system_prompt = f"Ты — умный ассистент. Контекст: {context}"
    return system_prompt


def generate_answer(user_query, relevant_docs):
    system_prompt = create_dynamic_prompt(user_query, relevant_docs)
    prompt = f"{system_prompt}\n\nQuestion: {user_query}\nAnswer:"
    messages = [
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": prompt}
    ]

    request_body = {
        "modelUri": "gpt://b1g72uajlds114mlufqi/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": messages
    }

    headers = get_auth_headers()
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers,
                             data=json.dumps(request_body))

    if response.status_code != 200:
        raise RuntimeError(
            f'Invalid response received: code: {response.status_code}, message: {response.text}'
        )

    response_data = response.json()
    answer = response_data.get("choices", [{}])[0].get("text", "")

    return answer, relevant_docs[0].url if relevant_docs else ""


@app.post("/assist", response_model=Response)
async def assist(query: Query):
    similar_docs = vector_store.hybrid_search(query.query, top_n=5)
    if not similar_docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    answer, source_url = generate_answer(query.query,
                                         [Document(id=row.id, title=row.title, description=row.description, url=row.url)
                                          for row in similar_docs])

    return {"text": answer, "links": [source_url]}


if __name__ == "__main__":
    query = "Как посмотреть лимиты счета?"

    session = SessionLocal()
    relevant_docs = session.query(Document).all()
    session.close()

    answer, source_url = generate_answer(query, relevant_docs)
    print(f"Answer: {answer}")
    print(f"Source URL: {source_url}")
