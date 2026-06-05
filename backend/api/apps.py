import os
import joblib
from django.apps import AppConfig




class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    anomaly_model = None

    def ready(self):
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "models",
                "anomaly_model.pkl"
            )
            if os.path.exists(model_path):
                ApiConfig.anomaly_model = joblib.load(model_path)
                print(f"Anomaly model loaded from {model_path}")
            else:
                print(f"Warning: No model found at {model_path} — run train_model first")
        except Exception as e:
            print(f"Warning: Could not load anomaly model — {str(e)}")