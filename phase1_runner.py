import sys
import os
from reportlab.pdfgen import canvas
from app.ingestion.loader import PDFLoader
from app.extraction.regex_extractor import RegexExtractor
from app.storage.db import init_db, get_db
from app.storage.models import Document, ExtractedData
from app.core.config import setup_logger

logger = setup_logger("runner")

def generate_sample_pdf(filename: str):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "INVOICE #12345")
    c.drawString(100, 730, "Date: 2023-12-15")
    c.drawString(100, 710, "Vendor: Acme Corp")
    c.drawString(100, 690, "Item A: $500.00")
    c.drawString(100, 670, "Item B: $750.50")
    c.drawString(100, 650, "Total Amount Due: $1,250.50")
    c.save()
    logger.info(f"Generated sample PDF: {filename}")

def run_pipeline(filename: str):
    # 1. Init DB
    init_db()
    
    # 2. Ingestion
    logger.info(f"Processing {filename}...")
    loader = PDFLoader(filename)
    if loader.detect_ocr_needed():
        logger.warning("OCR detected as needed (not implemented in Phase 1), proceeding with text extraction anyway.")
    
    text = loader.load_text()
    if not text:
        logger.error("No text extracted!")
        return

    # 3. Extraction
    extractor = RegexExtractor(text)
    data = extractor.extract_all()
    logger.info(f"Extracted Data: {data}")
    
    # 4. Storage
    db = next(get_db())
    try:
        doc = Document(filename=filename, text_content=text)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        extraction = ExtractedData(
            document_id=doc.id,
            total_amount=data["total_amount"],
            date=data["date"],
            extraction_method="regex",
            confidence=1.0 if (data["total_amount"] and data["date"]) else 0.5
        )
        db.add(extraction)
        db.commit()
        logger.info("Saved to database successfully.")
        
        # Verify
        saved = db.query(ExtractedData).filter(ExtractedData.document_id == doc.id).first()
        logger.info(f"DB Verification -> ID: {saved.id}, Amount: {saved.total_amount}")
        
    finally:
        db.close()

if __name__ == "__main__":
    sample_file = "data/sample_invoice.pdf"
    os.makedirs("data", exist_ok=True)
    generate_sample_pdf(sample_file)
    run_pipeline(sample_file)
