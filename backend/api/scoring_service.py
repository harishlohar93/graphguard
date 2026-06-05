import pandas as pd
from api.apps import ApiConfig
from api.neo4j_service import Neo4jService
from api.feature_extractor import GraphFeatureExtractor


class ScoringService:

    FEATURE_COLUMNS = [
        "degree_centrality",
        "in_degree_centrality",
        "pagerank",
        "clustering_coefficient",
        "follower_count",
        "following_count",
        "follow_velocity",
    ]

    @staticmethod
    def get_label(score):
        if score >= 0.8:
            return "bot"
        elif score >= 0.6:
            return "suspect"
        else:
            return "normal"

    @classmethod
    def score_single_account(cls, account_id):
        try:
            if ApiConfig.anomaly_model is None:
                raise RuntimeError(
                    "Model not loaded. Run python manage.py train_model first."
                )

            result = Neo4jService.run_query("""
                MATCH (a:Account {id: $account_id})
                OPTIONAL MATCH (a)-[:FOLLOWS]->(following)
                OPTIONAL MATCH (follower)-[:FOLLOWS]->(a)
                WITH a,
                     count(DISTINCT following) AS following_count,
                     count(DISTINCT follower) AS follower_count
                RETURN a.id AS id,
                       a.username AS username,
                       a.account_type AS account_type,
                       a.created_days_ago AS created_days_ago,
                       follower_count,
                       following_count,
                       a.post_count AS post_count
            """, {"account_id": account_id})

            if not result:
                raise RuntimeError(f"Account {account_id} not found in Neo4j")

            account = result[0]

            extractor = GraphFeatureExtractor()
            extractor.load_graph_from_neo4j()

            full_df = extractor.extract_features()

            account_row = full_df[full_df["account_id"] == account_id]

            if account_row.empty:
                raise RuntimeError(
                    f"Could not extract features for account {account_id}"
                )

            X = account_row[cls.FEATURE_COLUMNS].values
            raw_scores = ApiConfig.anomaly_model.decision_function(X)

            full_X = full_df[cls.FEATURE_COLUMNS].values
            all_raw = ApiConfig.anomaly_model.decision_function(full_X)
            normalized = float(
                1 - (raw_scores[0] - all_raw.min()) /
                (all_raw.max() - all_raw.min())
            )

            return {
                "account_id": account_id,
                "username": account["username"],
                "anomaly_score": round(normalized, 4),
                "label": cls.get_label(normalized),
            }

        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Scoring failed for {account_id}: {str(e)}")

    @classmethod
    def score_all_accounts(cls):
        try:
            if ApiConfig.anomaly_model is None:
                raise RuntimeError(
                    "Model not loaded. Run python manage.py train_model first."
                )

            extractor = GraphFeatureExtractor()
            df = extractor.extract_features()

            full_X = df[cls.FEATURE_COLUMNS].values
            raw_scores = ApiConfig.anomaly_model.decision_function(full_X)
            normalized = 1 - (raw_scores - raw_scores.min()) / (
                raw_scores.max() - raw_scores.min()
            )

            df["anomaly_score"] = normalized
            df["label"] = df["anomaly_score"].apply(cls.get_label)

            return df

        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Bulk scoring failed: {str(e)}")