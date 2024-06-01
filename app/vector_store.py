from sqlalchemy.sql import text
from app.database import SessionLocal, Document
import openai
from config import API_KEY


class VectorStore:
    def __init__(self):
        openai.api_key = API_KEY

    def embed_text(self, text):
        response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
        return response["data"][0]["embedding"]

    def add_to_index(self, title, description, url):
        embedding = self.embed_text(description)
        doc = Document(title=title, description=description, url=url, embedding=embedding)
        session = SessionLocal()
        session.add(doc)
        session.commit()
        session.close()

    def hybrid_search(self, query, top_n=5):
        query_vector = self.embed_text(query)
        session = SessionLocal()
        result = session.execute(
            text("""
                SELECT id, title, description, url, embedding <=> :query_vector AS distance
                FROM documents
                ORDER BY distance ASC
                LIMIT :top_n
            """),
            {"query_vector": query_vector, "top_n": top_n}
        ).fetchall()
        session.close()
        return result
