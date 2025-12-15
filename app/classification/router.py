from typing import Tuple
from app.classification.rules import RuleBasedClassifier
from app.classification.ml_model import MLClassifier

class ClassifierRouter:
    def __init__(self, use_ml: bool = True):
        self.rules = RuleBasedClassifier()
        self.ml_classifier = MLClassifier() if use_ml else None
        
    def classify(self, text: str) -> Tuple[str, float, str]:
        """
        Returns (class, confidence, method_used)
        """
        # 1. Try Rules (High Precision)
        cat_rules, conf_rules = self.rules.classify(text)
        
        # Threshold for rules? 
        # If we have strong keyword match (conf >= 0.6 corresponding to 2+ keywords roughly)
        if conf_rules >= 0.6:
            return cat_rules, conf_rules, "rules"
            
        # 2. Try ML
        if self.ml_classifier:
            cat_ml, conf_ml = self.ml_classifier.classify(text)
            return cat_ml, conf_ml, "ml"
            
        return "Unknown", 0.0, "none"
