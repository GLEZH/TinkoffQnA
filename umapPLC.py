import pandas as pd
import umap.umap_ as umap
import json

# Путь к файлу с данными
json_file_path = r"C:\Users\glezh\PycharmProjects\TinkoffQnA\data\dataset.json"

# Считываем данные из JSON файла
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

# Преобразуем данные в DataFrame
fmnist = pd.DataFrame(data)

# Преобразовываем данные, исключая столбец 'data' (в данном случае, вероятно 'description')
embedding = umap.UMAP(n_neighbors=5).fit_transform(fmnist.drop(['id'], axis=1))

# Для вывода результата
print(embedding)
