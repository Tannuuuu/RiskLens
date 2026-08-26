import numpy as np
from typing import List, Tuple, Optional
from app.ml.model import FraudModel
from app.config import get_settings

class FraudScoringEngine:
    def __init__(self, model: FraudModel):
        self.model = model
        self.settings = get_settings()
    
    def score_transaction(self, features: dict) -> Tuple[float, bool]:
        X = self._prepare_features(features)
        predictions, fraud_scores = self.model.predict(X)
        
        fraud_score = float(fraud_scores[0])
        is_fraud = bool(predictions[0] == -1)
        is_flagged = fraud_score >= self.settings.FRAUD_THRESHOLD
        
        return fraud_score, is_fraud, is_flagged
    
    def score_batch(self, transactions: List[dict]) -> List[Tuple[float, bool, bool]]:
        results = []
        for transaction in transactions:
            fraud_score, is_fraud, is_flagged = self.score_transaction(transaction)
            results.append((fraud_score, is_fraud, is_flagged))
        return results
    
    def _prepare_features(self, features: dict) -> np.ndarray:
        feature_list = []
        
        if self.model.feature_columns:
            for col in self.model.feature_columns:
                if col in features:
                    feature_list.append(features[col])
                else:
                    feature_list.append(0.0)
        else:
            feature_list = list(features.values())
        
        X = np.array([feature_list])
        
        if X.shape[1] != len(self.model.feature_columns):
            padded = np.zeros((1, len(self.model.feature_columns)))
            padded[0, :X.shape[1]] = X[0, :X.shape[1]]
            X = padded
        
        return X
    
    def get_risk_level(self, fraud_score: float) -> str:
        if fraud_score >= 0.9:
            return "critical"
        elif fraud_score >= 0.7:
            return "high"
        elif fraud_score >= 0.5:
            return "medium"
        else:
            return "low"
