# Financial Document Extraction System

A production-ready pipeline for extracting structured data from financial documents (Invoices, Receipts, Bank Statements) using a hybrid approach (Rule-based + ML + LLM) and OCR.

## Features
- **Multi-Format Ingestion**: Supports digital PDFs (`pdfplumber`) and scanned images (`pytesseract`).
- **Hybrid Classification**: Pattern matching for precision, failing over to TF-IDF+LogReg for recall.
- **Robust Extraction**:
  - **Regex**: Fast extraction for standard formats.
  - **LLM Fallback**: OpenAI (GPT-3.5 JSON mode) for complex layouts or missing fields.
- **REST API**: FastAPI backend for integration.
- **Database**: SQLite storage with SQLAlchemy ORM.

## Architecture
```mermaid
graph TD
    A[PDF Upload] --> B{Is Scanned?}
    B -- Yes --> C[OCR (Tesseract)]
    B -- No --> D[Digital Extraction]
    C --> E[Clean Text]
    D --> E
    E --> F{Classification}
    F --> G[Regex Extraction]
    G --> H{Critical Fields Found?}
    H -- Yes --> I[Store in DB]
    H -- No --> J[LLM Fallback (OpenAI)]
    J --> I
```

## Setup

1. **Prerequisites**
   - Python 3.10+
   - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and in System PATH.
   - [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) (for `pdf2image`) in System PATH.

2. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment**
   Set your OpenAI Key (optional, for fallback):
   ```bash
   $env:OPENAI_API_KEY="sk-..."
   ```

## Usage

**1. Run the API**
```bash
python -m app.api.main
# OR
uvicorn app.api.main:app --reload
```

**2. Test with CLI Runner**
```bash
python phase1_runner.py
```

**3. Train Classifier**
```bash
python train_ml.py
```

**4. Evaluate**
```bash
python evaluate.py
```

## API Documentation
POST `/extract`
- **Input**: `file` (PDF)
- **Output**:
  ```json
  {
      "filename": "invoice.pdf",
      "document_type": "Invoice",
      "total_amount": 1250.00,
      "date": "2023-12-15",
      "method": "rules + regex"
  }
  ```
