"""Neo4j Database Connection Manager."""

import logging
from contextlib import contextmanager
from typing import Generator, Any
from neo4j import GraphDatabase, Driver, Session
from src.config import settings

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Thread-safe Singleton wrapper around the Neo4j driver."""

    _instance: "Neo4jConnection | None" = None
    _driver: Driver | None = None

    def __new__(cls) -> "Neo4jConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_driver(self) -> Driver:
        """Returns or initializes the Neo4j Driver instance."""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
                    max_connection_lifetime=3600,
                    max_connection_pool_size=50,
                    connection_acquisition_timeout=30.0,
                )
                logger.info("Neo4j driver initialized successfully for %s", settings.NEO4J_URI)
            except Exception as e:
                logger.error("Failed to initialize Neo4j driver: %s", e)
                raise
        return self._driver

    def verify_connectivity(self) -> bool:
        """Verifies active connectivity to the Neo4j database."""
        try:
            driver = self.get_driver()
            driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error("Neo4j connectivity verification failed: %s", e)
            return False

    def close(self) -> None:
        """Closes the Neo4j driver pool."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j driver connection closed.")

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Provides a managed Neo4j Session context."""
        driver = self.get_driver()
        session = driver.session(database=settings.NEO4J_DATABASE)
        try:
            yield session
        finally:
            session.close()

    def execute_query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Executes a Cypher read/write query and returns records as dicts."""
        with self.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]


@contextmanager
def get_neo4j_session() -> Generator[Session, None, None]:
    """Helper context manager to obtain a Neo4j session directly."""
    conn = Neo4jConnection()
    with conn.session() as session:
        yield session
