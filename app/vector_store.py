from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import LlamaIndex


class VectorStore:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name='paraphrase-MiniLM-L6-v2')  # Замените на актуальную модель
        self.index = LlamaIndex()

    def embed_text(self, text):
        return self.embedding_model.embed(text)

    def add_to_index(self, text, doc_id):
        vector = self.embed_text(text)
        self.index.add(vector, doc_id)

    def search(self, query_vector, k=5):
        return self.index.search(query_vector, k)
