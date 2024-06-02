import pandas as pd
import tiktoken
import json
from openai import OpenAI

# Укажите ваш API ключ OpenAI
api_key = ""
client = OpenAI(api_key=api_key)

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

embedding_encoding = "cl100k_base"
max_tokens = 8000  # Максимум для text-embedding-3-small - 8191

# Загрузка и просмотр датасета из JSON файла
input_datapath = r"C:\Users\glezh\PycharmProjects\TinkoffQnA\data\dataset.json"
with open(input_datapath, 'r', encoding='utf-8') as f:
    data = json.load(f)["data"]

# Преобразование JSON данных в DataFrame
df = pd.json_normalize(data)
df = df[["title", "description"]]
df = df.dropna()
df["combined"] = "Title: " + df.title.str.strip() + "; Content: " + df.description.str.strip()
print(df.head(2))

# Выборка 1k самых последних отзывов и удаление слишком длинных образцов
top_n = 1000
df["index"] = df.index  # добавим индекс для сортировки
df = df.sort_values("index").tail(top_n * 2)  # Сначала обрежем до первых 2k записей, предполагая, что менее половины будут отфильтрованы
df.drop("index", axis=1, inplace=True)

encoding = tiktoken.get_encoding(embedding_encoding)

# Исключение отзывов, которые слишком длинные для встраивания
df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
df = df[df.n_tokens <= max_tokens].tail(top_n)
print(len(df))

# Получение встраиваний с использованием модели text-embedding-ada-002
df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))

print(df.head(2))
