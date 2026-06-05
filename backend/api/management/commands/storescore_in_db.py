from django.core.management.base import BaseCommand
from api.scoring_service import ScoringService
from api.models import Account, Alert


class Command(BaseCommand):
    help = "Score all accounts and save results to PostgreSQL"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Scoring all accounts...")
            df = ScoringService.score_all_accounts()

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
                    continue
                except Exception as e:
                    self.stdout.write(f"Warning: {row['account_id']} — {str(e)}")
                    skipped += 1
                    continue

            self.stdout.write(f"\nSaved: {saved} alerts")
            self.stdout.write(f"Skipped: {skipped} accounts not in PostgreSQL")

            bot_count = df[df["label"] == "bot"].shape[0]
            suspect_count = df[df["label"] == "suspect"].shape[0]
            normal_count = df[df["label"] == "normal"].shape[0]

            self.stdout.write(f"\nBot:     {bot_count}")
            self.stdout.write(f"Suspect: {suspect_count}")
            self.stdout.write(f"Normal:  {normal_count}")

            self.stdout.write(self.style.SUCCESS("\nDone."))

        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))