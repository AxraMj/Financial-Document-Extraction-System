from app.classification.classifier_base import BaseClassifier
from typing import Tuple

class RuleBasedClassifier(BaseClassifier):
    def __init__(self):
        self.keywords = {
            "Invoice": ["invoice", "bill to", "due date", "balance due"],
            "Receipt": ["receipt", "payment received", "transaction", "card number"],
            "Bank Statement": ["statement", "account summary", "opening balance", "closing balance"]
        }

    def classify(self, text: str) -> Tuple[str, float]:
        text_lower = text.lower()
        
        scores = {category: 0 for category in self.keywords}
        
        for category, phrases in self.keywords.items():
            for phrase in phrases:
                if phrase in text_lower:
                    scores[category] += 1
        
        # Get max score
        best_category = max(scores, key=scores.get)
        score = scores[best_category]
        
        # Heuristic confidence
        # If score > 0, we have some matched keywords. 
        # Normalize slightly? For now just use score as raw indicator, 
        # but map to 0.0-1.0 roughly.
        if score == 0:
            return "Unknown", 0.0
        
        confidence = min(score * 0.3, 0.95) # Cap at 0.95, need 3+ keywords for high confidence
        return best_category, confidence
