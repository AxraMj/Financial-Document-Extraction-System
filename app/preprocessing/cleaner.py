import re

class TextCleaner:
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Replaces multiple spaces/newlines with single space."""
        return re.sub(r'\s+', ' ', text).strip()
    
    @staticmethod
    def clean_currency(amount_str: str) -> float:
        """Converts currency string to float."""
        # Remove '$', ',', ' ' 
        cleaned = re.sub(r'[^\d.]', '', amount_str)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
