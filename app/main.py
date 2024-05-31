from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
from app.vector_store import VectorStore
from app.llm_model import generate_answer
from app.database import Document, create_db_and_tables, add_document, get_document_by_id

app = FastAPI()


class Query(BaseModel):
    query: str


class Response(BaseModel):
    text: str
    links: list[str]


vector_store = VectorStore()
create_db_and_tables()


@app.post("/assist", response_model=Response)
async def assist(query: Query):
    question_vector = vector_store.embed_text(query.query)
    similar_docs = vector_store.search(question_vector)
    if not similar_docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    sources = [get_document_by_id(doc_id) for doc_id in similar_docs]
    answer, source_url = generate_answer(query.query, "Ты — умный ассистент.", sources)

    return {"text": answer, "links": [source_url]}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Assistant API",
        version="0.1.0",
        description="API для помощника на основе YandexGPT",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
