from django.core.management.base import BaseCommand
from api.feature_extractor import GraphFeatureExtractor
from api.anomaly_detector import AnomalyDetector


class Command(BaseCommand):
    help = "Train anomaly detection model on graph features"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Step 1 — Extracting features from PostgreSQL...")
            
            from api.models import Account
            import pandas as pd
            import numpy as np
            
            accounts = Account.objects.all().values(
                'account_id', 'username', 'account_type',
                'follower_count', 'following_count', 
                'post_count', 'created_days_ago'
            )
            
            rows = []
            for acc in accounts:
                created_days = acc['created_days_ago'] or 1
                velocity = (acc['following_count'] or 0) / created_days
                
                rows.append({
                    'account_id': acc['account_id'],
                    'username': acc['username'],
                    'account_type': acc['account_type'],
                    'degree_centrality': 0.0,
                    'in_degree_centrality': 0.0,
                    'pagerank': 0.0,
                    'clustering_coefficient': 0.0,
                    'follower_count': acc['follower_count'] or 0,
                    'following_count': acc['following_count'] or 0,
                    'created_days_ago': created_days,
                    'follow_velocity': round(velocity, 4),
                })
            
            df = pd.DataFrame(rows)
            self.stdout.write(f"Features extracted for {len(df)} accounts")

            self.stdout.write("Step 2 — Training Isolation Forest model...")
            from api.anomaly_detector import AnomalyDetector
            detector = AnomalyDetector(model_path="models/anomaly_model.pkl")
            detector.train(df)

            self.stdout.write("Step 3 — Scoring all accounts...")
            scores = detector.score(df)
            df["anomaly_score"] = scores

            self.stdout.write("Step 4 — Saving model to disk...")
            detector.save()

            self.stdout.write("\n--- Top 10 highest scoring accounts ---")
            top = df.nlargest(10, "anomaly_score")[
                ["account_id", "username", "account_type", "anomaly_score"]
            ]
            self.stdout.write(str(top))

            bot_avg = df[df["account_type"] == "bot"]["anomaly_score"].mean()
            normal_avg = df[df["account_type"] == "normal"]["anomaly_score"].mean()

            self.stdout.write(f"\nAverage bot score:    {bot_avg:.4f}")
            self.stdout.write(f"Average normal score: {normal_avg:.4f}")

            self.stdout.write(self.style.SUCCESS("\nDone. Model trained and saved."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))