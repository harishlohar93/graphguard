from django.core.management.base import BaseCommand
from api.feature_extractor import GraphFeatureExtractor
from api.anomaly_detector import AnomalyDetector


class Command(BaseCommand):
    help = "Train anomaly detection model on graph features"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Step 1 — Extracting features from Neo4j graph...")
            extractor = GraphFeatureExtractor()
            df = extractor.extract_features()

            self.stdout.write("Step 2 — Training Isolation Forest model...")
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

            self.stdout.write(self.style.SUCCESS(
                "\nDone. Model trained and saved successfully."
            ))
            

        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))