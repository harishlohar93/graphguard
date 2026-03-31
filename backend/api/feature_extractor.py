import networkx as nx
import pandas as pd
from api.neo4j_service import Neo4jService


class GraphFeatureExtractor:

    def __init__(self):
        self.graph = None
        self.accounts_data = []

    def load_graph_from_neo4j(self):
        try:
            self.accounts_data = Neo4jService.run_query("""
                MATCH (a:Account)
                RETURN a.id AS id,
                       a.username AS username,
                       a.account_type AS account_type,
                       a.follower_count AS follower_count,
                       a.following_count AS following_count,
                       a.post_count AS post_count,
                       a.created_days_ago AS created_days_ago
            """)

            edges_data = Neo4jService.run_query("""
                MATCH (a:Account)-[:FOLLOWS]->(b:Account)
                RETURN a.id AS source, b.id AS target
            """)

            self.graph = nx.DiGraph()

            for account in self.accounts_data:
                self.graph.add_node(account["id"], **account)

            for edge in edges_data:
                self.graph.add_edge(edge["source"], edge["target"])

            print(f"Graph loaded: {self.graph.number_of_nodes()} nodes, "
                  f"{self.graph.number_of_edges()} edges")

        except Exception as e:
            raise RuntimeError(f"Failed to load graph from Neo4j: {str(e)}")

    def extract_features(self):
        try:
            if self.graph is None:
                self.load_graph_from_neo4j()

            print("Computing degree centrality...")
            degree_centrality = nx.degree_centrality(self.graph)

            print("Computing in-degree centrality...")
            in_degree_centrality = nx.in_degree_centrality(self.graph)

            print("Computing PageRank...")
            pagerank = nx.pagerank(self.graph, alpha=0.85)

            print("Computing clustering coefficient...")
            clustering = nx.clustering(self.graph.to_undirected())

            rows = []
            for account in self.accounts_data:
                try:
                    acc_id = account["id"]

                    created_days = account.get("created_days_ago", 0)
                    following = account.get("following_count", 0)

                    if created_days and created_days > 0:
                        velocity = following / created_days
                    else:
                        velocity = 0.0

                    rows.append({
                        "account_id": acc_id,
                        "username": account.get("username", "unknown"),
                        "account_type": account.get("account_type", "normal"),
                        "degree_centrality": round(degree_centrality.get(acc_id, 0.0), 6),
                        "in_degree_centrality": round(in_degree_centrality.get(acc_id, 0.0), 6),
                        "pagerank": round(pagerank.get(acc_id, 0.0), 6),
                        "clustering_coefficient": round(clustering.get(acc_id, 0.0), 6),
                        "follower_count": account.get("follower_count", 0),
                        "following_count": account.get("following_count", 0),
                        "created_days_ago": account.get("created_days_ago", 0),
                        "follow_velocity": round(velocity, 4),
                    })

                except Exception as e:
                    print(f"Warning: skipping account {account.get('id', 'unknown')} — {str(e)}")
                    continue

            if not rows:
                raise RuntimeError("No features extracted — rows list is empty")

            df = pd.DataFrame(rows)

            null_count = df.isnull().sum().sum()
            if null_count > 0:
                print(f"Warning: {null_count} null values found — filling with 0")
                df = df.fillna(0)

            print(f"Feature extraction complete: {len(df)} accounts, "
                  f"{len(df.columns)} features")

            return df

        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Feature extraction failed: {str(e)}")