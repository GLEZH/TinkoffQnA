import json
import openai

# Установите свой API ключ
openai.api_key = ''

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_embeddings(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=[text],  # Обратите внимание на формат input
        model=model
    )
    return response['data'][0]['embedding']

def vectorize_dataset(dataset):
    for item in dataset['data']:
        # Объединяем все текстовые поля, которые хотим векторизовать
        text_to_vectorize = ' '.join([
            item.get('title', ''),
            item.get('description', ''),
            item.get('parent_title', '')
        ])

        # Получаем векторное представление
        embedding = get_embeddings(text_to_vectorize)
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

    # Векторизация данных
    vectorized_dataset = vectorize_dataset(dataset)

    # Сохранить векторизованные данные обратно в JSON файл
    save_json(vectorized_dataset, output_filepath)
    print(f"Vectorized data saved to {output_filepath}")
