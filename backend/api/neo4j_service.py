from neo4j import GraphDatabase
from django.conf import settings


class Neo4jService:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            from django.conf import settings
            if not settings.NEO4J_URI or not settings.NEO4J_PASSWORD:
                raise RuntimeError("Neo4j not configured")
            cls._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        return cls._driver


    @classmethod
    def close(cls):
        if cls._driver is not None:
            cls._driver.close()
            cls._driver = None

    @classmethod
    def run_query(cls, query, parameters=None):
        driver = cls.get_driver()
        with driver.session() as session:

            def _execute(tx):
                result = tx.run(query, parameters or {})
                return [record.data() for record in result]
            
            return session.execute_write(_execute)
