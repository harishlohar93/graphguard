from django.core.management.base import BaseCommand
from api.models import Account, Alert
import pandas as pd
import joblib
import os


class Command(BaseCommand):
    help = "Score all accounts and save results to PostgreSQL"

    def get_label(self, score):
        if score >= 0.8:
            return "bot"
        elif score >= 0.6:
            return "suspect"
        return "normal"

    def handle(self, *args, **options):
        try:
            model_path = "models/anomaly_model.pkl"
            if not os.path.exists(model_path):
                self.stdout.write(self.style.ERROR("Model not found — run train_model first"))
                return

            model = joblib.load(model_path)
            self.stdout.write("Model loaded successfully")

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
                    'follower_count': acc['follower_count'] or 0,
                    'following_count': acc['following_count'] or 0,
                    'created_days_ago': created_days,
                    'follow_velocity': round(velocity, 4),
                    'degree_centrality': 0.0,
                    'in_degree_centrality': 0.0,
                    'pagerank': 0.0,
                    'clustering_coefficient': 0.0,
                })

            df = pd.DataFrame(rows)

            FEATURE_COLUMNS = [
                "degree_centrality", "in_degree_centrality", "pagerank",
                "clustering_coefficient", "follower_count", "following_count",
                "follow_velocity",
            ]

            X = df[FEATURE_COLUMNS].values
            raw_scores = model.decision_function(X)
            normalized = 1 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min())
            df["anomaly_score"] = normalized
            df["label"] = df["anomaly_score"].apply(self.get_label)

            saved = 0
            skipped = 0

            for _, row in df.iterrows():
                try:
                    account = Account.objects.get(account_id=row["account_id"])
                    Alert.objects.update_or_create(
                        account=account,
                        defaults={
                            "score": row["anomaly_score"],
                            "label": row["label"],
                            "status": "pending",
                        }
                    )
                    saved += 1
                except Account.DoesNotExist:
                    skipped += 1
                except Exception as e:
                    self.stdout.write(f"Warning: {row['account_id']} — {str(e)}")
                    skipped += 1

            self.stdout.write(f"Saved: {saved} alerts")
            self.stdout.write(f"Skipped: {skipped}")
            self.stdout.write(self.style.SUCCESS("Done."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))