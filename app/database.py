from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Document

DATABASE_URL = "sqlite:///./test.db"  # Replace with your database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def add_document(doc_data):
    db = SessionLocal()
    doc = Document(**doc_data)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    db.close()
    return doc

def get_document_by_id(doc_id):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == doc_id).first()
    db.close()
    return doc
