import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from app.core.config import setup_logger

logger = setup_logger("llm_extractor")

class LLMExtractor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
             logger.warning("OPENAI_API_KEY not found. LLM extraction will fail if called.")
        
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def extract(self, text: str, doc_type: str) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("OpenAI Client not initialized. Missing API Key.")

        prompt = self._get_prompt(text, doc_type)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106", # Efficient model with JSON mode
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant. Extract structured data from the provided document text in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f"LLM Extraction failed: {e}")
            return {}

    def _get_prompt(self, text: str, doc_type: str) -> str:
        return f"""
        Extract the following fields from this {doc_type}:
        - total_amount (float, e.g. 1200.50)
        - date (ISO 8601 string YYYY-MM-DD or null)
        - vendor (string or null)
        - currency (string, e.g. USD, EUR)
        
        Document Text:
        {text[:4000]}  # Truncate to avoid context limit issues in this MVP
        """
