"""Dense Embedding Clients for FAISS Vector Store.

Supports Ollama embedding endpoint (/api/embed) with batching,
L2 normalization for cosine similarity, and multi-model switching.
"""

import logging
from typing import Sequence
import httpx
import numpy as np
from src.config import settings

logger = logging.getLogger(__name__)


class OllamaEmbeddingClient:
    """Client for generating dense vector embeddings using Ollama."""

    def __init__(self, model_name: str | None = None, base_url: str | None = None, timeout: float = 60.0):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._dim: int | None = None

    @property
    def dimension(self) -> int:
        """Returns the embedding dimension of the configured model."""
        if self._dim is None:
            sample_vec = self.embed_query("ping")
            self._dim = len(sample_vec)
        return self._dim

    def embed_query(self, text: str, normalize: bool = True) -> np.ndarray:
        """Generates embedding for a single query string.
        
        Returns:
            np.ndarray of shape (dim,), dtype float32.
        """
        vecs = self.embed_documents([text], batch_size=1, normalize=normalize)
        return vecs[0]

    def embed_documents(
        self,
        texts: Sequence[str],
        batch_size: int = 16,
        normalize: bool = True
    ) -> np.ndarray:
        """Generates embeddings for a list of documents with batching.
        
        Returns:
            np.ndarray of shape (len(texts), dim), dtype float32.
        """
        if not texts:
            return np.empty((0, 0), dtype=np.float32)

        all_embeddings: list[list[float]] = []

        with httpx.Client(timeout=self.timeout) as client:
            for i in range(0, len(texts), batch_size):
                batch = list(texts[i : i + batch_size])
                payload = {
                    "model": self.model_name,
                    "input": batch,
                    "keep_alive": "60m",
                    "options": {
                        "num_ctx": 512
                    }
                }
                try:
                    res = client.post(f"{self.base_url}/api/embed", json=payload)
                    if res.status_code == 200:
                        batch_embeds = res.json().get("embeddings", [])
                        all_embeddings.extend(batch_embeds)
                    else:
                        logger.error(f"Ollama embed error {res.status_code}: {res.text}")
                        # Fallback to single requests via /api/embeddings if /api/embed fails
                        batch_embeds = self._embed_batch_fallback(client, batch)
                        all_embeddings.extend(batch_embeds)
                except Exception as e:
                    logger.error(f"Failed to embed batch {i}..{i+len(batch)}: {e}")
                    batch_embeds = self._embed_batch_fallback(client, batch)
                    all_embeddings.extend(batch_embeds)

        matrix = np.array(all_embeddings, dtype=np.float32)

        if normalize and len(matrix) > 0:
            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1e-10
            matrix = matrix / norms

        if self._dim is None and len(matrix) > 0:
            self._dim = matrix.shape[1]

        return matrix

    def _embed_batch_fallback(self, client: httpx.Client, batch: list[str]) -> list[list[float]]:
        """Fallback to /api/embeddings single prompt calls if /api/embed fails."""
        results = []
        for text in batch:
            try:
                res = client.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.model_name, "prompt": text}
                )
                if res.status_code == 200:
                    results.append(res.json().get("embedding", []))
                else:
                    results.append([])
            except Exception:
                results.append([])
        return results


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    client = OllamaEmbeddingClient(model_name="bge-m3")
    print(f"Model: {client.model_name}, Dimension: {client.dimension}")
    vec = client.embed_query("ทดสอบสิทธิวันลาพักผ่อนประจำปี")
    print(f"Sample vector shape: {vec.shape}, norm: {np.linalg.norm(vec):.4f}")
