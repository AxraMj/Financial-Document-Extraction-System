import pdfplumber
from pathlib import Path
from typing import Optional
from app.core.config import setup_logger

logger = setup_logger(__name__)

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def extract_text_ocr(self) -> str:
        """Extracts text from scanned PDF using OCR (Tesseract)."""
        logger.info("Starting OCR extraction...")
        try:
            import pytesseract
            from pdf2image import convert_from_path
            
            # Check if tesseract is available? 
            # pytesseract raises TesseractNotFoundError if not found usually.
            
            images = convert_from_path(str(self.file_path))
            text_content = []
            
            for i, image in enumerate(images):
                logger.debug(f"OCR processing page {i+1}...")
                text = pytesseract.image_to_string(image)
                text_content.append(text)
            
            return "\n".join(text_content)
            
        except ImportError as e:
            logger.error(f"OCR dependencies missing: {e}. Install pytesseract and pdf2image/poppler.")
            raise
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise

    def load_text(self, force_ocr: bool = False) -> str:
        """
        Extracts text. Uses native text if best, otherwise falls back to OCR.
        """
        ocr_needed = self.detect_ocr_needed() or force_ocr
        
        if ocr_needed:
            logger.info(f"Using OCR for {self.file_path.name}")
            return self.extract_text_ocr()
        else:
            return self.extract_text_native()

    def extract_text_native(self) -> str:
        text_content = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                    else:
                        logger.warning(f"Page {idx+1} yielded no text (possible scanned page).")
            
            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"Failed to load PDF: {e}")
            raise
    def detect_ocr_needed(self) -> bool:
        """
        Simple heuristic: check if text density is very low.
        For Phase 1, we just return False and log if it looks suspicious.
        """
        try:
            with pdfplumber.open(self.file_path) as pdf:
                if not pdf.pages:
                    return False
                # Check first page
                text = pdf.pages[0].extract_text() or ""
                if len(text.strip()) < 50: # Arbitrary threshold
                    logger.info("Low text density detected. OCR might be needed.")
                    return True
                return False
        except Exception:
            return True
