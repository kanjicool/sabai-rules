"""Knowledge Graph Seeder: Populates Neo4j from Cypher scripts and JSON definitions."""

import sys
import logging
from pathlib import Path
from src.config import settings
from src.graph.connection import Neo4jConnection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("graph_seeder")


def parse_cypher_file(file_path: Path) -> list[str]:
    """Parses a .cypher file into individual executable statements."""
    if not file_path.exists():
        raise FileNotFoundError(f"Cypher script not found: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    statements: list[str] = []
    current_stmt: list[str] = []

    for line in content.splitlines():
        trimmed = line.strip()
        # Skip empty lines or pure single-line comments
        if not trimmed or trimmed.startswith("//"):
            continue
        current_stmt.append(line)
        if trimmed.endswith(";"):
            stmt_text = "\n".join(current_stmt).strip()
            # Remove trailing semicolon
            if stmt_text.endswith(";"):
                stmt_text = stmt_text[:-1].strip()
            if stmt_text:
                statements.append(stmt_text)
            current_stmt = []

    # Catch any dangling statement without semicolon
    if current_stmt:
        stmt_text = "\n".join(current_stmt).strip()
        if stmt_text:
            statements.append(stmt_text)

    return statements


def seed_schema(conn: Neo4jConnection, schema_path: Path) -> None:
    """Applies constraints and indexes defined in schema.cypher."""
    logger.info("Applying constraints and indexes from: %s", schema_path.name)
    statements = parse_cypher_file(schema_path)

    with conn.session() as session:
        for stmt in statements:
            try:
                session.run(stmt)
                logger.debug("Executed schema stmt: %s", stmt.splitlines()[0])
            except Exception as e:
                logger.warning("Schema statement notice (%s): %s", e, stmt.splitlines()[0])

    logger.info("Schema applied successfully (%d statements processed).", len(statements))


def seed_knowledge_graph(conn: Neo4jConnection, cypher_path: Path) -> None:
    """Ingests full HR benefits graph nodes and relationships."""
    logger.info("Seeding Knowledge Graph from: %s", cypher_path.name)
    statements = parse_cypher_file(cypher_path)

    with conn.session() as session:
        for idx, stmt in enumerate(statements, start=1):
            try:
                session.run(stmt)
                logger.debug("[%d/%d] Ingested block successfully", idx, len(statements))
            except Exception as e:
                logger.error("Error executing statement #%d: %s\nStatement:\n%s", idx, e, stmt)
                raise

    logger.info("Knowledge Graph seeded successfully (%d statement blocks executed).", len(statements))


def inspect_graph_stats(conn: Neo4jConnection) -> dict[str, int]:
    """Returns total counts of nodes and relationships in the database."""
    node_query = "MATCH (n) RETURN count(n) AS total_nodes"
    rel_query = "MATCH ()-[r]->() RETURN count(r) AS total_relationships"

    with conn.session() as session:
        nodes = session.run(node_query).single()["total_nodes"]
        rels = session.run(rel_query).single()["total_relationships"]

    labels_query = "CALL db.labels() YIELD label RETURN label"
    with conn.session() as session:
        labels = [r["label"] for r in session.run(labels_query)]

    logger.info("================ GRAPH DATABASE SUMMARY ================")
    logger.info("Total Nodes: %d", nodes)
    logger.info("Total Relationships: %d", rels)
    logger.info("Active Labels (%d): %s", len(labels), ", ".join(labels))
    logger.info("========================================================")

    return {"total_nodes": nodes, "total_relationships": rels, "label_count": len(labels)}


def run_seed() -> bool:
    """Main orchestration for seeding the database."""
    conn = Neo4jConnection()
    if not conn.verify_connectivity():
        logger.error("Cannot connect to Neo4j at %s. Please check credentials or start the container.", settings.NEO4J_URI)
        return False

    schema_file = settings.KG_DIR / "schema.cypher"
    data_file = settings.KG_DIR / "primo_knowledge_graph.cypher"

    seed_schema(conn, schema_file)
    seed_knowledge_graph(conn, data_file)
    inspect_graph_stats(conn)
    return True


if __name__ == "__main__":
    success = run_seed()
    sys.exit(0 if success else 1)
