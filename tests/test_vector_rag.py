"""Pytest test suite for Vector RAG pipeline and FastAPI Webhook endpoints."""

import pytest
from src.vector.loader import PDFDocumentLoader
from src.vector.chunker import DocumentChunker
from src.vector.store import HRVectorStore
from src.rag.vector_rag import VectorRAGEngine
from src.webhook.server import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def vector_store():
    store = HRVectorStore()
    assert store.is_persisted(), "Vector store index must be built and persisted."
    return store


@pytest.fixture(scope="module")
def rag_engine(vector_store):
    return VectorRAGEngine(vector_store=vector_store)


@pytest.fixture(scope="module")
def api_client():
    return TestClient(app)


def test_pdf_loader():
    """Verify that PDF can be opened and extracted."""
    loader = PDFDocumentLoader()
    pages = loader.load_pages()
    assert len(pages) >= 40, f"Expected at least 40 pages, got {len(pages)}"
    assert "พรีโม" in pages[0].text or "ข้อบังคับ" in pages[0].text


def test_document_chunker():
    """Verify chunk generation, Small-to-Big linking, and metadata presence."""
    loader = PDFDocumentLoader()
    pages = loader.load_pages()[:3]
    chunker = DocumentChunker(chunk_size=400, chunk_overlap=50)
    chunks, parents = chunker.chunk_pages(pages)
    assert len(chunks) > 0
    assert len(parents) > 0
    first_chunk = chunks[0]
    assert first_chunk.page_number >= 1
    assert first_chunk.text != ""


def test_vector_store_search(vector_store):
    """Verify search returns top matches with relevant scores."""
    results = vector_store.search("วันหยุดพักผ่อนประจำปี", top_k=3)
    assert len(results) == 3
    assert results[0]["score"] > 0
    assert any("พักผ่อน" in r["text"] or "วันหยุด" in r["text"] for r in results)


def test_rag_engine_query(rag_engine):
    """Verify RAG engine returns formatted answer and citations."""
    ans = rag_engine.query("สิทธิ์การลาพักผ่อนประจำปี")
    assert ans.answer != ""
    assert len(ans.citations) > 0
    formatted = ans.format_line_text()
    assert "📋 คำตอบข้อบังคับพนักงาน:" in formatted
    assert "📌 ข้อมูลอ้างอิงจากเอกสาร:" in formatted


def test_fastapi_health_endpoint(api_client):
    """Verify GET /health returns 200 OK."""
    response = api_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["vector_index_ready"] is True


def test_fastapi_local_ask_endpoint(api_client):
    """Verify POST /ask returns valid RAG answer payload."""
    response = api_client.post("/ask", json={"query": "กองทุนสำรองเลี้ยงชีพ", "top_k": 2})
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "answer" in data
    assert "citations" in data
    assert len(data["citations"]) > 0


def test_dynamic_top_k_selector():
    """Verify DynamicTopKSelector adjusts k according to query complexity."""
    from src.rag.vector_rag import DynamicTopKSelector
    # Simple query
    k_simple = DynamicTopKSelector.select_k("ทดลองงานกี่วัน")
    assert k_simple == 2, f"Expected k=2 for simple query, got {k_simple}"
    
    # Complex overview query
    k_complex = DynamicTopKSelector.select_k("มีสิทธิประโยชน์และวันลาทั้งหมดกี่ประเภท และมีเงื่อนไขอย่างไรบ้าง")
    assert k_complex >= 4, f"Expected k>=4 for complex query, got {k_complex}"


def test_token_budget_manager():
    """Verify TokenBudgetManager prevents context overflow."""
    from src.rag.vector_rag import TokenBudgetManager
    manager = TokenBudgetManager(max_context_tokens=300)
    fake_hits = [
        {"page_number": 1, "chapter": "ทดสอบ", "text": "ข้อความทดสอบ " * 50},
        {"page_number": 2, "chapter": "ทดสอบ", "text": "ข้อความทดสอบ " * 50},
        {"page_number": 3, "chapter": "ทดสอบ", "text": "ข้อความทดสอบ " * 50},
    ]
    context, hits, tokens = manager.pack_context(fake_hits)
    assert tokens <= 350, f"Token budget exceeded limit: {tokens}"
    assert len(hits) >= 1


def test_bm25_and_hybrid_search(vector_store):
    """Verify BM25 search and Hybrid FAISS+BM25 RRF fusion."""
    bm25_hits = vector_store._search_bm25_raw("ลาพักร้อน ระดับ 3", candidate_k=3)
    assert len(bm25_hits) == 3
    assert bm25_hits[0]["score"] > 0

    hybrid_hits = vector_store._search_hybrid("ลาพักร้อน ระดับ 3", candidate_k=3)
    assert len(hybrid_hits) == 3
    assert hybrid_hits[0]["score"] > 0

