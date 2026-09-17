"""Vector RAG Module for Sabai-Rules LINE Chatbot.

This module coordinates:
- Document vector similarity retrieval (top-k relevant sections)
- Context augmentation and citation tracking (page numbers & chapters)
- LLM inference and response synthesis
- LINE text and Flex Message card formatting
"""

from src.rag.vector_rag import VectorRAGEngine, RAGAnswer

__all__ = [
    "VectorRAGEngine",
    "RAGAnswer",
]
