import re
from typing import Optional, Dict, Any
from app.preprocessing.cleaner import TextCleaner
from app.core.config import setup_logger

logger = setup_logger(__name__)

class RegexExtractor:
    def __init__(self, text: str):
        self.text = text
        self.clean_text = TextCleaner.normalize_whitespace(text)

    def extract_total_amount(self) -> Optional[float]:
        """
        Attempts to find total amount using keywords + currency pattern.
        """
        # Look for "Total", "Amount Due", "Grand Total" followed by currency
        # Patterns: 
        # 1. (Total|Amount|Balance).*?(\$?\d{1,3}(,\d{3})*(\.\d{2})?)
        
        patterns = [
            r'(?:Total|Amount Due|Grand Total|Balance Due)[\s\w]*?[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'[\$]\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)' # Aggressive: any dollar sign
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                 # Get the last match as it's often the total at the bottom
                candidate = matches[-1]
                try:
                    return TextCleaner.clean_currency(candidate)
                except ValueError:
                    continue
        return None

    def extract_date(self) -> Optional[str]:
        """
        Extracts dates in formats: DD/MM/YYYY, YYYY-MM-DD, Month DD, YYYY
        """
        # Simple patterns
        patterns = [
            r'\b(\d{4}-\d{2}-\d{2})\b', # 2023-12-01
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b', # 01/12/2023
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b' # Dec 1, 2023
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE)
            if match:
                return match.group(0) # Return matched string directly for now
        return None

    def extract_all(self) -> Dict[str, Any]:
        return {
            "total_amount": self.extract_total_amount(),
            "date": self.extract_date(),
            "method": "regex"
        }
