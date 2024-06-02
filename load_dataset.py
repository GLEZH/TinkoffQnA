import json
from app.database import add_document
from app.vector_store import VectorStore

vector_store = VectorStore()

def load_data(filepath: str):
    with open(filepath, 'r') as file:
        data = json.load(file)['data']
        for entry in data:
            doc = add_document({
                'id': entry['id'],
                'title': entry['title'],
                'url': entry['url'],
                'source': entry['source'],
                'business_line_id': entry['business_line_id'],
                'direction': entry['direction'],
                'product': entry['product'],
                'type': entry['type'],
                'description': entry['description'],
                'parent_title': entry['parent_title'],
                'parent_url': entry['parent_url']
            })
            vector_store.add_to_index(entry['description'], doc.id)

if __name__ == "__main__":
    load_data('data/dataset.json')
