"""LLM Client for Vector RAG Answering.

Interacts with local Ollama instance (e.g. Qwen2.5 / Typhoon) or provides
graceful fallback generation based on retrieved context.
"""

import json
import logging
from typing import Any
import httpx
from src.config import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for generating responses using local Ollama LLM."""

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    def is_available(self) -> bool:
        """Checks if local Ollama server is running and reachable."""
        try:
            with httpx.Client(timeout=2.0) as client:
                res = client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generates a grounded text completion from Ollama using /api/chat for superior Thai output."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "keep_alive": "60m",
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_ctx": 4096,
                "num_predict": 650,
            }
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                res = client.post(f"{self.base_url}/api/chat", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    content = data.get("message", {}).get("content", "").strip()
                    if content:
                        return content
                logger.warning(f"Ollama returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Could not reach Ollama at {self.base_url}: {e}")

        # Fallback synthesizer if Ollama is offline
        return self._rule_based_fallback(prompt)

    def _rule_based_fallback(self, prompt: str) -> str:
        """Graceful fallback summary if LLM service is offline."""
        return (
            "⚠️ [ระบบทำงานในโหมด Offline Fallback - เนื่องจากยังไม่ได้เปิด Ollama]\n\n"
            "ข้อมูลที่สืบค้นได้จากเอกสารข้อบังคับการทำงาน PRIMO:\n"
            + self._extract_summary_from_prompt(prompt)
        )

    def _extract_summary_from_prompt(self, prompt: str) -> str:
        """Extracts key snippet lines from the grounded context in the prompt."""
        lines = prompt.splitlines()
        context_lines = []
        capture = False
        for line in lines:
            if "=== เนื้อหาจากเอกสาร" in line:
                capture = True
                continue
            if "=== สิ้นสุดเนื้อหา" in line:
                capture = False
                continue
            if capture and line.strip():
                context_lines.append(line.strip())

        if context_lines:
            # Return first few salient lines
            snippet = "\n".join(context_lines[:6])
            return f"{snippet}\n\n💡 (แนะนำ: เปิด Ollama ด้วยคำสั่ง `ollama run qwen2.5:7b` เพื่อให้ AI สรุปสำนวนอัตโนมัติ)"
        return "พบข้อมูลที่เกี่ยวข้องในเอกสารข้อบังคับ แต่ไม่สามารถติดต่อ Ollama เพื่อสรุปได้ในขณะนี้"


if __name__ == "__main__":
    client = OllamaClient()
    print(f"Ollama Available: {client.is_available()} at {client.base_url}")
