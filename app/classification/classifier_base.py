from abc import ABC, abstractmethod
from typing import Tuple

class BaseClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Returns (predicted_class, confidence_score)
        """
        pass
