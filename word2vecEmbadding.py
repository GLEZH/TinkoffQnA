import json
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import numpy as np

# Загрузите ресурсы NLTK
nltk.download('punkt')
nltk.download('stopwords')

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def preprocess_text(text):
    stop_words = set(stopwords.words('russian'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return filtered_tokens

def train_word2vec(corpus):
    model = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4)
    return model

def get_text_embedding(text, model):
    tokens = preprocess_text(text)
    embeddings = [model.wv[word] for word in tokens if word in model.wv]
    if embeddings:
        return np.mean(embeddings, axis=0).tolist()
    else:
        return np.zeros(model.vector_size).tolist()

def vectorize_dataset(dataset, model):
    for item in dataset['data']:
        text_to_vectorize = ' '.join([
            item.get('title', ''),
            item.get('description', ''),
            item.get('parent_title', '')
        ])
        embedding = get_text_embedding(text_to_vectorize, model)
        item['embedding'] = embedding
    return dataset

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Загрузить данные из JSON файла
    input_filepath = r'C:\Users\glezh\PycharmProjects\TinkoffQnA\data\dataset.json'
    output_filepath = 'output.json'
    dataset = load_json(input_filepath)

    # Подготовка текстов для обучения Word2Vec
    corpus = []
    for item in dataset['data']:
        text_to_vectorize = ' '.join([
            item.get('title', ''),
            item.get('description', ''),
            item.get('parent_title', '')
        ])
        corpus.append(preprocess_text(text_to_vectorize))

    # Обучение модели Word2Vec
    word2vec_model = train_word2vec(corpus)

    # Векторизация данных
    vectorized_dataset = vectorize_dataset(dataset, word2vec_model)

    # Сохранить векторизованные данные обратно в JSON файл
    save_json(vectorized_dataset, output_filepath)
    print(f"Vectorized data saved to {output_filepath}")
