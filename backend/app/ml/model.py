import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os
from datetime import datetime

class FraudModel:
    def __init__(self, model_path: str = "trained_models"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_columns = None
        
    def load_data(self, data_path: str) -> pd.DataFrame:
        df = pd.read_csv(data_path)
        if 'Time' in df.columns and 'Amount' in df.columns:
            df['Normalized_Amount'] = self._normalize_amount(df['Amount'])
            df['Hour'] = (df['Time'] % 86400) / 3600
        return df
    
    def _normalize_amount(self, amounts: pd.Series) -> np.ndarray:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        return scaler.fit_transform(amounts.values.reshape(-1, 1)).flatten()
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        if 'Class' in df.columns:
            feature_cols = [c for c in df.columns if c not in ['Class', 'Time', 'Amount']]
        else:
            feature_cols = [c for c in df.columns if c not in ['Time', 'Amount']]
        
        self.feature_columns = feature_cols
        X = df[feature_cols].values
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled
    
    def train(self, data_path: str, contamination: float = 0.001):
        print(f"Loading data from {data_path}...")
        df = self.load_data(data_path)
        print(f"Dataset shape: {df.shape}")
        
        X = self.prepare_features(df)
        print(f"Features shape: {X.shape}")
        
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            max_samples='auto',
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        print("Training Isolation Forest model...")
        self.model.fit(X)
        
        predictions = self.model.predict(X)
        anomaly_scores = self.model.decision_function(X)
        
        df['predictions'] = predictions
        df['anomaly_scores'] = anomaly_scores
        
        if 'Class' in df.columns:
            y_true = df['Class'].values
            y_pred = (predictions == -1).astype(int)
            
            precision = precision_score(y_true, y_pred, zero_division=0)
            recall = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            
            try:
                auc_roc = roc_auc_score(y_true, -anomaly_scores)
            except:
                auc_roc = 0.0
            
            metrics = {
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'auc_roc': auc_roc,
                'training_samples': len(df),
                'fraud_ratio': float(y_true.sum() / len(y_true)),
                'model_version': f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            print(f"\nModel Metrics:")
            print(f"Precision: {precision:.4f}")
            print(f"Recall: {recall:.4f}")
            print(f"F1 Score: {f1:.4f}")
            print(f"AUC-ROC: {auc_roc:.4f}")
        else:
            metrics = {
                'training_samples': len(df),
                'model_version': f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        
        self.save_model()
        
        return metrics
    
    def save_model(self):
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.model, os.path.join(self.model_path, 'isolation_forest.joblib'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.joblib'))
        joblib.dump(self.feature_columns, os.path.join(self.model_path, 'feature_columns.joblib'))
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        self.model = joblib.load(os.path.join(self.model_path, 'isolation_forest.joblib'))
        self.scaler = joblib.load(os.path.join(self.model_path, 'scaler.joblib'))
        self.feature_columns = joblib.load(os.path.join(self.model_path, 'feature_columns.joblib'))
        print("Model loaded successfully")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        if self.scaler is not None:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X
        
        predictions = self.model.predict(X_scaled)
        scores = self.model.decision_function(X_scaled)
        
        fraud_scores = 1 / (1 + np.exp(scores))
        
        return predictions, fraud_scores
    
    def evaluate(self, data_path: str) -> dict:
        df = self.load_data(data_path)
        X = self.prepare_features(df)
        
        predictions, fraud_scores = self.predict(X)
        
        if 'Class' in df.columns:
            y_true = df['Class'].values
            y_pred = (predictions == -1).astype(int)
            
            return {
                'precision': precision_score(y_true, y_pred, zero_division=0),
                'recall': recall_score(y_true, y_pred, zero_division=0),
                'f1': f1_score(y_true, y_pred, zero_division=0),
                'auc_roc': roc_auc_score(y_true, -fraud_scores),
                'total_samples': len(df),
                'fraud_detected': int(y_pred.sum()),
                'actual_fraud': int(y_true.sum())
            }
        
        return {'error': 'No ground truth labels available'}
