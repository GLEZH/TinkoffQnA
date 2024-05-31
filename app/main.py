from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.vector_store import VectorStore
from app.llm_model import generate_answer
from app.database import Document, create_db_and_tables, add_document, get_document_by_id

app = FastAPI()


class Query(BaseModel):
    question: str
    system_prompt: str


vector_store = VectorStore()
create_db_and_tables()


@app.post("/ask")
async def ask_question(query: Query):
    question_vector = vector_store.embed_text(query.question)
    similar_docs = vector_store.search(question_vector)
    if not similar_docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    sources = [get_document_by_id(doc_id) for doc_id in similar_docs]
    answer = generate_answer(query.question, query.system_prompt, sources)

    return {"answer": answer, "sources": sources}
