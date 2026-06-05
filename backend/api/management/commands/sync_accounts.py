from django.core.management.base import BaseCommand
from api.neo4j_service import Neo4jService
from api.models import Account


class Command(BaseCommand):
    help = "Sync accounts from Neo4j into PostgreSQL"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Fetching accounts from Neo4j...")
            accounts = Neo4jService.run_query("""
                MATCH (a:Account)
                RETURN a.id AS account_id,
                       a.username AS username,
                       a.account_type AS account_type,
                       a.follower_count AS follower_count,
                       a.following_count AS following_count,
                       a.post_count AS post_count,
                       a.created_days_ago AS created_days_ago
            """)

            created = 0
            updated = 0

            for acc in accounts:
                try:
                    _, was_created = Account.objects.update_or_create(
                        account_id=acc["account_id"],
                        defaults={
                            "username": acc["username"],
                            "account_type": acc["account_type"],
                            "follower_count": acc["follower_count"] or 0,
                            "following_count": acc["following_count"] or 0,
                            "post_count": acc["post_count"] or 0,
                            "created_days_ago": acc["created_days_ago"] or 0,
                            "is_flagged": acc["account_type"] != "normal",
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1
                except Exception as e:
                    self.stdout.write(
                        f"Warning: skipping {acc.get('account_id')} — {str(e)}"
                    )
                    continue

            self.stdout.write(f"Created: {created} accounts")
            self.stdout.write(f"Updated: {updated} accounts")
            self.stdout.write(self.style.SUCCESS("Sync complete."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))