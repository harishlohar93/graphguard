import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Account

fake = Faker()

class Command(BaseCommand):
    help = "Seed fake accounts directly into PostgreSQL"

    def handle(self, *args, **options):
        try:
            if Account.objects.count() > 0:
                self.stdout.write("Accounts already exist — skipping")
                return

            self.stdout.write("Creating 450 normal accounts...")
            for i in range(450):
                Account.objects.create(
                    account_id=f"acc_{i}",
                    username=fake.user_name(),
                    created_days_ago=random.randint(100, 2000),
                    follower_count=random.randint(50, 5000),
                    following_count=random.randint(30, 1000),
                    post_count=random.randint(10, 500),
                    account_type="normal",
                    is_flagged=False
                )

            self.stdout.write("Creating 50 bot accounts...")
            for i in range(450, 500):
                Account.objects.create(
                    account_id=f"acc_{i}",
                    username=fake.user_name(),
                    created_days_ago=random.randint(1, 10),
                    follower_count=random.randint(2000, 8000),
                    following_count=random.randint(3000, 8000),
                    post_count=random.randint(500, 2000),
                    account_type="bot",
                    is_flagged=True
                )

            self.stdout.write(self.style.SUCCESS(
                f"Done. {Account.objects.count()} accounts created."
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))