from typing import Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pickle

class BiasDetectorLevel2:
    """
    Second-pass strict bias detection
    Uses ML classifier trained on offensive content
    More sensitive than Level 1
    """
    
    def __init__(self, model_path: str = None):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = SVC(probability=True, kernel='rbf')
        self.model_path = model_path
        
        if model_path:
            self.load_model(model_path)
    
    async def analyze_email(self, email_text: str) -> Dict:
        """
        More rigorous analysis than Level 1
        Returns strict bias score
        """
        
     
        features = self.vectorizer.transform([email_text])
        
     
        prediction = self.classifier.predict(features)[0]
        probability = self.classifier.predict_proba(features)[0][1]
        
   
        if probability > 0.7:  
            recommendation = "ESCALATE_TO_HUMAN"
        elif probability > 0.5:
            recommendation = "ESCALATE_TO_HUMAN"
        else:
            recommendation = "APPROVED_TO_SEND"
        
        return {
            "bias_score": float(probability),
            "flags": self._get_specific_issues(email_text),
            "recommendation": recommendation,
            "model_name": "BiasDetectorLevel2",
            "confidence": float(probability)
        }
    
    def _get_specific_issues(self, text: str) -> list:
      
        issues = []
      
        return issues
    
    def train(self, training_data: list, labels: list):
        """
        Train on labeled dataset of biased vs non-biased emails
        """
        features = self.vectorizer.fit_transform(training_data)
        self.classifier.fit(features, labels)
    
    def save_model(self, path: str):
        pickle.dump((self.vectorizer, self.classifier), open(path, 'wb'))
    
    def load_model(self, path: str):
        self.vectorizer, self.classifier = pickle.load(open(path, 'rb'))