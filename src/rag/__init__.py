"""Hybrid RAG Orchestration Module (Phase 3).

This module coordinates:
- Intent classification & Entity extraction from user question
- Dual-retrieval: Neo4j (deterministic rules) + FAISS (narrative text)
- Context fusion and synthesis
- Response formatting for LINE Flex Message cards
"""
