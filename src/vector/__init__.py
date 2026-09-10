"""Vector Store and Text Chunking Module (Phase 2).

This module handles:
- PDF Text Extraction from 47-page Primo PDF using PyMuPDF / fitz
- Recursive & section-aware chunking preserving Thai context
- Multilingual sentence embeddings (sentence-transformers / paraphrase-multilingual-MiniLM-L12-v2)
- Local FAISS vector index storage and retrieval
"""
