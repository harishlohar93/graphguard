import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.neo4j_service import Neo4jService

fake = Faker()


class Command(BaseCommand):
    help = "Seed Neo4j with fake social graph data"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing graph...")
        Neo4jService.run_query("MATCH (n) DETACH DELETE n")

        self.stdout.write("Creating 450 normal accounts...")
        for i in range(450):
            Neo4jService.run_query("""
                CREATE (:Account {
                    id: $id,
                    username: $username,
                    created_days_ago: $age,
                    follower_count: $followers,
                    following_count: $following,
                    post_count: $posts,
                    account_type: 'normal'
                })
            """, {
                "id": f"acc_{i}",
                "username": fake.user_name(),
                "age": random.randint(100, 2000),
                "followers": random.randint(50, 5000),
                "following": random.randint(30, 1000),
                "posts": random.randint(10, 500),
            })

        self.stdout.write("Creating 50 bot accounts...")
        for i in range(450, 500):
            Neo4jService.run_query("""
                CREATE (:Account {
                    id: $id,
                    username: $username,
                    created_days_ago: $age,
                    follower_count: $followers,
                    following_count: $following,
                    post_count: $posts,
                    account_type: 'bot'
                })
            """, {
                "id": f"acc_{i}",
                "username": fake.user_name(),
                "age": random.randint(1, 10),
                "followers": random.randint(2000, 8000),
                "following": random.randint(3000, 8000),
                "posts": random.randint(500, 2000),
            })

        self.stdout.write("Creating follow relationships for normal accounts...")
        normal_ids = [f"acc_{i}" for i in range(450)]
        for acc_id in normal_ids:
            targets = random.sample(normal_ids, random.randint(3, 15))
            for target in targets:
                if target != acc_id:
                    Neo4jService.run_query("""
                        MATCH (a:Account {id: $from_id})
                        MATCH (b:Account {id: $to_id})
                        CREATE (a)-[:FOLLOWS]->(b)
                    """, {"from_id": acc_id, "to_id": target})

        self.stdout.write("Creating dense follow relationships for bot accounts...")
        bot_ids = [f"acc_{i}" for i in range(450, 500)]
        for bot_id in bot_ids:
            targets = random.sample(bot_ids, 40)
            for target in targets:
                if target != bot_id:
                    Neo4jService.run_query("""
                        MATCH (a:Account {id: $from_id})
                        MATCH (b:Account {id: $to_id})
                        CREATE (a)-[:FOLLOWS]->(b)
                    """, {"from_id": bot_id, "to_id": target})

        self.stdout.write(self.style.SUCCESS(
            "Done! 500 accounts and relationships created in Neo4j."
        ))
