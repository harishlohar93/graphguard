from django.core.management.base import BaseCommand
from api.feature_extractor import GraphFeatureExtractor


class Command(BaseCommand):
    help = "Extract graph features from Neo4j for all accounts"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Starting feature extraction...")

            extractor = GraphFeatureExtractor()
            df = extractor.extract_features()

            self.stdout.write("\n--- Top 5 accounts by follow velocity ---")
            top_velocity = df.nlargest(5, "follow_velocity")[
                ["account_id", "username", "account_type", "follow_velocity"]
            ]
            self.stdout.write(str(top_velocity))

            self.stdout.write("\n--- Top 5 accounts by clustering coefficient ---")
            top_clustering = df.nlargest(5, "clustering_coefficient")[
                ["account_id", "username", "account_type", "clustering_coefficient"]
            ]
            self.stdout.write(str(top_clustering))

            self.stdout.write("\n--- Top 5 accounts by pagerank ---")
            top_pagerank = df.nlargest(5, "pagerank")[
                ["account_id", "username", "account_type", "pagerank"]
            ]
            self.stdout.write(str(top_pagerank))

            self.stdout.write(self.style.SUCCESS(
                f"\nDone. {len(df)} accounts processed."
            ))

        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))