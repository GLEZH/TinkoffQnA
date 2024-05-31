from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    url = Column(String)
    source = Column(String)
    business_line_id = Column(String)
    direction = Column(String)
    product = Column(String)
    type = Column(String)
    description = Column(Text)
    parent_title = Column(String)
    parent_url = Column(String)
