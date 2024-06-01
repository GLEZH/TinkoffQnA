from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.database import SessionLocal, Document
import gensim.downloader as api
import numpy as np
from config import API_KEY


class VectorStore:
    def __init__(self):
        self.model = api.load("word2vec-google-news-300")  # Load pre-trained Word2Vec model

    def embed_text(self, text):
        words = text.split()
        word_vectors = [self.model[word] for word in words if word in self.model]
        if not word_vectors:
            return np.zeros(300)
        return np.mean(word_vectors, axis=0)

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
            {"query_vector": query_vector.tolist(), "top_n": top_n}
        ).fetchall()
        session.close()
        return result
