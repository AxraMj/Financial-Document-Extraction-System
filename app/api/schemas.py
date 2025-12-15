from pydantic import BaseModel
from typing import Optional

class ExtractionResponse(BaseModel):
    filename: str
    document_type: str
    confidence: float
    total_amount: Optional[float]
    date: Optional[str]
    processing_time: float
    method: str
