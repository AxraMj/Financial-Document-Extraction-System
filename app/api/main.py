import time
import shutil
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.ingestion.loader import PDFLoader
from app.preprocessing.cleaner import TextCleaner
from app.extraction.regex_extractor import RegexExtractor
from app.classification.router import ClassifierRouter
from app.api.schemas import ExtractionResponse
from app.core.config import setup_logger

logger = setup_logger("api")

app = FastAPI(title="Financial Document Extraction System")

# Initialize components
classifier = ClassifierRouter(use_ml=True)

@app.post("/extract", response_model=ExtractionResponse)
async def extract_document(file: UploadFile = File(...)):
    start_time = time.time()
    
    # Validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save temp file
    temp_path = f"data/temp_{file.filename}"
    os.makedirs("data", exist_ok=True)
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Ingestion
        loader = PDFLoader(temp_path)
        text = loader.load_text()
        
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        # 2. Classification
        doc_type, conf, clf_method = classifier.classify(text)
        
        # 3. Extraction Strategy
        # Base extraction (Regex)
        extractor = RegexExtractor(text)
        data = extractor.extract_all()
        
        extraction_method = "regex"
        
        # Check if we need to fallback to LLM
        # Conditions: 
        # - Total Amount is missing
        # - OR Date is missing
        # - OR Confidence is low (implied by missing fields)
        
        if data.get("total_amount") is None or data.get("date") is None:
            logger.info("Regex failed to extract critical fields. Attempting LLM fallback...")
            
            from app.extraction.llm_extractor import LLMExtractor
            llm = LLMExtractor()
            
            # Only call if we have an API Key (handled inside class, but being explicit here helps flow)
            if llm.client:
                llm_data = llm.extract(text, doc_type)
                
                # Merge/Override
                if llm_data:
                    data.update(llm_data)
                    extraction_method = "llm_fallback"
            else:
                logger.warning("LLM fallback needed but no API key available.")

        return ExtractionResponse(
            filename=file.filename,
            document_type=doc_type,
            confidence=conf,
            total_amount=data.get("total_amount"),
            date=data.get("date"),
            processing_time=time.time() - start_time,
            method=f"{clf_method} + {extraction_method}"
        )

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
def health_check():
    return {"status": "ok", "version": "0.2.0"}
