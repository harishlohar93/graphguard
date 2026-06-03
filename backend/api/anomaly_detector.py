import joblib
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


class AnomalyDetector:

    FEATURE_COLUMNS = [
        "degree_centrality",
        "in_degree_centrality",
        "pagerank",
        "clustering_coefficient",
        "follower_count",
        "following_count",
        "follow_velocity",
    ]

    def __init__(self, model_path="models/anomaly_model.pkl"):
        self.model_path = model_path
        self.model = None

    def train(self, df):
        try:
            X = df[self.FEATURE_COLUMNS].values
            self.model = IsolationForest(
                n_estimators=100,
                contamination=0.1,
                random_state=42
            )
            self.model.fit(X)
            print(f"Model trained on {len(X)} accounts")
            return self
        except Exception as e:
            raise RuntimeError(f"Training failed: {str(e)}")

    def score(self, df):
        try:
            if self.model is None:
                raise RuntimeError("Model not trained yet")
            X = df[self.FEATURE_COLUMNS].values
            raw_scores = self.model.decision_function(X)
            normalized = 1 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min())
            return normalized
        except Exception as e:
            raise RuntimeError(f"Scoring failed: {str(e)}")

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            print(f"Model saved to {self.model_path}")
        except Exception as e:
            raise RuntimeError(f"Save failed: {str(e)}")

    def load(self):
        try:
            if not os.path.exists(self.model_path):
                raise RuntimeError(f"No model found at {self.model_path}")
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
            return self
        except Exception as e:
            raise RuntimeError(f"Load failed: {str(e)}")