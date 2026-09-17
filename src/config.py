"""Configuration settings for Sabai-Rules application."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings loaded from environment or .env file."""

    # Project Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    KG_DIR: Path = DATA_DIR / "knowledge_graph"

    # Neo4j Settings
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "SecretPassword123"
    NEO4J_DATABASE: str = "neo4j"

    # Vector & Embeddings
    EMBEDDING_MODEL_NAME: str = "bge-m3"
    FAISS_INDEX_PATH: str = "data/faiss_index"
    VECTOR_INDEX_BACKEND: str = "faiss"  # "faiss" or "tfidf"

    # RAG Accuracy Improvements
    ENABLE_HYBRID_SEARCH: bool = True
    ENABLE_RERANKING: bool = True
    ENABLE_QUERY_EXPANSION: bool = True
    ENABLE_HYDE: bool = False
    ENABLE_PARENT_RETRIEVAL: bool = True

    # LLM Settings (Vector RAG)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    # LINE Messaging API (Planned Phase)
    LINE_CHANNEL_SECRET: str = ""
    LINE_CHANNEL_ACCESS_TOKEN: str = ""

    # Webhook Server & Public Tunnel URL
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    PUBLIC_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
