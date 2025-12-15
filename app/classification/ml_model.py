import pickle
from typing import Tuple, List
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from app.classification.classifier_base import BaseClassifier
import os

class MLClassifier(BaseClassifier):
    def __init__(self, model_path: str = "data/model.pkl"):
        self.model_path = model_path
        self.model = None
        self.classes = []

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")

    def train(self, texts: List[str], labels: List[str]):
        """
        Trains a TF-IDF + Logistic Regression pipeline
        """
        self.model = Pipeline([
            ('vect', CountVectorizer(stop_words='english', max_features=1000)),
            ('tfidf', TfidfTransformer()),
            ('clf', LogisticRegression(random_state=42))
        ])
        
        self.model.fit(texts, labels)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)

    def classify(self, text: str) -> Tuple[str, float]:
        if not self.model:
            try:
                self.load_model()
            except FileNotFoundError:
                return "Unknown", 0.0

        prediction = self.model.predict([text])[0]
        # Get probability
        probas = self.model.predict_proba([text])[0]
        max_proba = max(probas)
        
        return prediction, max_proba
