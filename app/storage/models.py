from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.storage.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    text_content = Column(Text, nullable=True)
    
    extractions = relationship("ExtractedData", back_populates="document")

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    total_amount = Column(Float, nullable=True)
    date = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    
    extraction_method = Column(String, default="regex") # regex, ml, llm
    confidence = Column(Float, default=0.0)
    
    document = relationship("Document", back_populates="extractions")
