"""Vector Store and Text Processing Module for Sabai-Rules.

This module handles:
- PDF Text Extraction from 47-page Primo PDF using PyMuPDF
- Semantic, section-aware chunking preserving Thai context
- High-performance vector storage, indexing, and similarity retrieval
"""

from src.vector.loader import PDFDocumentLoader, DocumentPage
from src.vector.chunker import DocumentChunker, TextChunk
from src.vector.store import HRVectorStore

__all__ = [
    "PDFDocumentLoader",
    "DocumentPage",
    "DocumentChunker",
    "TextChunk",
    "HRVectorStore",
]
