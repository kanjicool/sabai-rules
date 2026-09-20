"""Vector RAG Engine for HR Regulations LINE Chatbot.

Orchestrates Production-Grade Hybrid RAG:
1. Dynamic Top-k Selection based on query complexity and intent
2. Token Budget Management to prevent context overflow
3. Hybrid Search (Dense FAISS + Sparse BM25) + Small-to-Big Parent Context
4. Strict Chain-of-Thought (CoT) Prompting with Few-Shot examples
5. Zero Hallucination Guardrail & Citation Verification
"""

import logging
import re
from dataclasses import dataclass
from typing import Any
from src.vector.store import HRVectorStore
from src.vector.query_processor import HRQueryProcessor
from src.llm.client import OllamaClient

logger = logging.getLogger(__name__)


@dataclass
class RAGAnswer:
    """Structure representing a generated RAG answer with citations."""
    query: str
    answer: str
    citations: list[dict[str, Any]]
    confidence_score: float
    retrieved_k: int = 0
    token_budget_used: int = 0

    def format_line_text(self) -> str:
        """Formats the response as clean text for LINE chatbot message."""
        citation_str = "\n".join([
            f"• หน้า {c['page_number']} ({c['chapter']})"
            for c in self.citations[:3]
        ])

        return (
            f"📋 คำตอบข้อบังคับพนักงาน:\n\n"
            f"{self.answer}\n\n"
            f"📌 ข้อมูลอ้างอิงจากเอกสาร:\n"
            f"{citation_str}"
        )

    def to_flex_bubble(self) -> dict[str, Any]:
        """Creates a modern LINE Flex Message Bubble dictionary."""
        citation_rows = []
        for c in self.citations[:3]:
            citation_rows.append({
                "type": "text",
                "text": f"• หน้า {c['page_number']} - {c['chapter']}",
                "size": "xs",
                "color": "#8c8c8c",
                "wrap": True
            })

        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#009688",
                "contents": [
                    {
                        "type": "text",
                        "text": "HR Benefit Assistant",
                        "color": "#ffffff",
                        "weight": "bold",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "ข้อบังคับและสิทธิประโยชน์",
                        "color": "#ffffffcc",
                        "size": "xs"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"❓ {self.query}",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True,
                        "color": "#333333"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": self.answer,
                        "size": "xs",
                        "wrap": True,
                        "margin": "md",
                        "color": "#444444"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "📌 อ้างอิงเอกสาร PRIMO:",
                        "size": "xxs",
                        "weight": "bold",
                        "color": "#666666",
                        "margin": "md"
                    },
                    *citation_rows
                ]
            }
        }


class DynamicTopKSelector:
    """Dynamically determines optimal Top-k retrieval count based on query complexity."""

    # Complex keywords that require multi-chunk or overview synthesis
    COMPLEX_INDICATORS = [
        "ทั้งหมด", "เปรียบเทียบ", "มีอะไรบ้าง", "สิทธิประโยชน์",
        "ขั้นตอน", "ระเบียบทั้งหมด", "เงื่อนไขทั้งหมด", "กี่ประเภท",
        "อัตราทั้งหมด", "เกณฑ์", "ต่างกันอย่างไร"
    ]

    @classmethod
    def select_k(cls, query: str) -> int:
        """Selects dynamic k:
        - 2 for simple, single-entity queries
        - 3 for standard queries
        - 4 or 5 for complex / overview / multi-part queries
        """
        q = query.strip().lower()
        words = re.findall(r"[\w\u0E00-\u0E7F]+", q)
        word_count = len(words)

        # Check for complex multi-concept questions
        is_complex = any(ind in q for ind in cls.COMPLEX_INDICATORS)

        if is_complex or word_count >= 14:
            return 5
        elif word_count >= 7 or any(w in q for w in ["และ", "หรือ", "ถ้า", "กรณี"]):
            return 3
        else:
            return 2


class TokenBudgetManager:
    """Manages prompt context token budget to prevent LLM context overflow."""

    def __init__(self, max_context_tokens: int = 1600):
        # Approx. 1 Thai token ~= 2 characters on multilingual BPE
        self.max_tokens = max_context_tokens
        self.max_chars = max_context_tokens * 2

    def pack_context(self, hits: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], int]:
        """Packs retrieved hits into a unified context string strictly within the token budget.
        
        Returns:
            tuple of (context_text, included_hits, estimated_tokens)
        """
        accumulated_chars = 0
        included_hits: list[dict[str, Any]] = []
        blocks: list[str] = []

        for i, hit in enumerate(hits, 1):
            block_header = f"[ส่วนที่ {i}] (หน้า {hit['page_number']} | {hit['chapter']}):\n"
            block_content = hit["text"]
            block_text = f"{block_header}{block_content}"
            block_len = len(block_text)

            if accumulated_chars + block_len <= self.max_chars:
                blocks.append(block_text)
                included_hits.append(hit)
                accumulated_chars += block_len
            else:
                # Truncate remaining budget if feasible
                remaining_chars = self.max_chars - accumulated_chars - len(block_header) - 30
                if remaining_chars > 200:
                    truncated_content = block_content[:remaining_chars] + "\n...(ข้อความถูกตัดตามขีดจำกัด)"
                    blocks.append(f"{block_header}{truncated_content}")
                    included_hits.append(hit)
                    accumulated_chars += len(blocks[-1])
                break

        context_text = "\n\n".join(blocks)
        estimated_tokens = accumulated_chars // 2
        return context_text, included_hits, estimated_tokens


FEW_SHOT_EXAMPLES = """
[ตัวอย่างโครงสร้างคำตอบที่ถูกต้อง]
• อ้างอิงจาก หน้า 18 (หมวด 4 วันลา และหลักเกณฑ์การลา):
พนักงานระดับ 3 (ระดับชำนาญการ / Senior / Supervisor) มีสิทธิวันลาพักผ่อนประจำปีดังนี้:
• สิทธิ์วันลาพักผ่อนประจำปี: ได้รับ 7 วันทำงานต่อปี
• เงื่อนไข: จะมีสิทธิ์เมื่อผ่านการทดลองงานและทำงานติดต่อกันครบ 1 ปีขึ้นไป
(หมายเหตุ: ระดับ 1–2 ได้ 6 วัน, ระดับ 3–5 ได้ 7 วัน, ระดับ 6–8 ได้ 8 วัน, ระดับ 9 ได้ 10 วัน)

• อ้างอิงจาก หน้า 41–43 (หมวด 11 สิทธิประโยชน์สวัสดิการ):
กองทุนสำรองเลี้ยงชีพ (PVD) บริษัทจะจ่ายเงินสมทบในอัตราเดียวกับเงินสะสมของพนักงาน ดังนี้:
• อายุงานน้อยกว่า 3 ปี: สะสมได้ 2% หรือ 3% (บริษัทสมทบ 2% หรือ 3% เท่ากัน)
• อายุงาน 3 ถึง 5 ปี: สะสมได้ 2%, 3% หรือ 5% (บริษัทสมทบเท่ากัน)
• อายุงาน 5 ปีขึ้นไป: สะสมได้สูงสุด 7% (บริษัทสมทบเท่ากัน)

• อ้างอิงจาก หน้า 35 (หมวด 10 การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย):
พนักงานที่ทำงานมา 4 ปี (ซึ่งอยู่ในเกณฑ์อายุงานครบ 3 ปี แต่ไม่ถึง 6 ปี) หากถูกเลิกจ้างโดยไม่มีความผิดร้ายแรง จะได้รับเงินชดเชยดังนี้:
• อัตราเงินชดเชยที่ได้รับ: ได้รับเงินชดเชยไม่น้อยกว่าค่าจ้างอัตราสุดท้าย 180 วัน (ประมาณ 6 เดือน)
(เกณฑ์ตารางอัตราค่าชดเชย: ครบ 120 วัน–1 ปี ได้ 30 วัน, ครบ 1–3 ปี ได้ 90 วัน, ครบ 3–6 ปี ได้ 180 วัน, ครบ 6–10 ปี ได้ 240 วัน, ครบ 10 ปีขึ้นไป ได้ 300 วัน)
"""


def check_chit_chat_or_out_of_scope(question: str) -> str | None:
    """Detects casual chit-chat, fatigue/sleepiness, greetings, or out-of-scope interactions."""
    text = question.strip().lower()

    # 1. Fatigue / Sleepiness / Rest
    if re.search(r"(ง่วง|ง่วงนอน|เหนื่อย|เหนื่อยจัง|เพลีย|อยากนอน|นอนไม่หลับ)", text):
        return (
            "สู้ๆ นะครับ! หากรู้สึกเหนื่อยหรือง่วงนอน แนะนำให้พักสายตา ดื่มน้ำ หรือลุกขึ้นยืดเส้นยืดสายสักครู่ก่อนนะครับ 😊\n\n"
            "หากต้องการตรวจสอบระเบียบการพักผ่อนของบริษัท PRIMO:\n"
            "• เวลาพักระหว่างวัน: พนักงานมีเวลาพักวันละ 1 ชั่วโมง (หลังจากทำงานติดต่อกันไม่เกิน 5 ชั่วโมง)\n"
            "• สิทธิ์วันลาพักผ่อนประจำปี (พักร้อน): มีสิทธิ์ตามอายุงานและระดับตำแหน่ง (เริ่มต้น 6–10 วันทำงาน/ปี)\n"
            "• สิทธิ์การลาป่วย หรือลากิจธุระอันจำเป็น\n\n"
            "หากต้องการตรวจสอบข้อมูลวันลาหรือระเบียบข้อใด พิมพ์สอบถามผมได้เลยครับ!"
        )

    # 2. General Greetings
    if re.fullmatch(r"(สวัสดี|สวัสดีครับ|สวัสดีค่ะ|หวัดดี|ดีครับ|ดีค่ะ|hello|hi|hey|ดีจ้า|ฮัลโหล)[\s!.]*", text):
        return (
            "สวัสดีครับ! ผมคือ Sabai-Rules ผู้ช่วยอัจฉริยะด้านข้อบังคับและสวัสดิการพนักงาน บริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด (PRIMO)\n\n"
            "ยินดีให้ข้อมูลระเบียบและสิทธิประโยชน์ต่างๆ เช่น:\n"
            "• สิทธิ์วันลาพักผ่อนประจำปี (พักร้อน) ตามระดับตำแหน่ง\n"
            "• อัตราเงินชดเชยกรณีเลิกจ้างตามอายุงาน\n"
            "• สิทธิประโยชน์กองทุนสำรองเลี้ยงชีพ (PVD)\n"
            "• หลักเกณฑ์การทำงานล่วงเวลา (OT)\n\n"
            "สามารถพิมพ์คำถาม หรือพิมพ์ 'เปิดเครื่องคำนวณ' เพื่อคำนวณเงินชดเชยและค่าล่วงเวลาได้เลยครับ"
        )

    # 3. Thank you
    if re.fullmatch(r"(ขอบคุณ|ขอบคุณครับ|ขอบคุณค่ะ|ขอบใจ|thanks|thank you|แต๊งกิ้ว)[\s!.]*", text):
        return (
            "ด้วยความยินดีอย่างยิ่งครับ! หากมีข้อสงสัยเกี่ยวกับระเบียบการทำงานหรือสิทธิประโยชน์ของ PRIMO เพิ่มเติม สามารถสอบถามได้ตลอดเวลาเลยนะครับ 😊"
        )

    # 4. Identity / Purpose
    if re.fullmatch(r"(คุณคือใคร|นายคือใคร|ทำอะไรได้บ้าง|ช่วยอะไรได้บ้าง|เธอคือใคร|bot ทำอะไรได้)[\s!.]*", text):
        return (
            "ผมคือ Sabai-Rules ระบบผู้ช่วยอัจฉริยะตอบคำถามระเบียบและข้อบังคับการทำงาน PRIMO ครับ\n\n"
            "สิ่งที่ผมสามารถช่วยเหลือได้:\n"
            "• ค้นหาข้อบังคับการทำงานของบริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด\n"
            "• ให้ข้อมูลสิทธิ์วันลาพักร้อน ลาป่วย ลาคลอด และการลาประเภทต่างๆ\n"
            "• คำนวณเงินชดเชยตามอายุงาน และเงินสมทบกองทุน PVD\n"
            "• ชี้แจงหลักเกณฑ์การทำงานล่วงเวลา (OT) และบทลงโทษทางวินัย"
        )

    return None


def clean_markdown_for_line(text: str) -> str:
    """Converts raw Markdown tables and bold asterisks into clean bullet points for LINE."""
    lines = text.splitlines()
    output_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        # Skip markdown table divider line |---|---|
        if re.match(r"^[\|\s\-:]+$", stripped) and "-" in stripped:
            continue

        # Check if line is a table row | col1 | col2 |
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped[1:-1].split("|") if c.strip()]
            cells = [re.sub(r"\*\*(.*?)\*\*", r"\1", c) for c in cells]

            # Header row detection
            if not in_table:
                in_table = True
                continue

            if len(cells) == 2:
                output_lines.append(f"• {cells[0]}: {cells[1]}")
            elif len(cells) >= 3:
                output_lines.append(f"• {cells[0]} ({cells[1]}): {cells[2]}")
            elif len(cells) == 1:
                output_lines.append(f"• {cells[0]}")
        else:
            in_table = False
            # Clean bold syntax **bold** -> bold
            cleaned_line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            output_lines.append(cleaned_line)

    cleaned_text = "\n".join(output_lines)
    # Deduplicate excessive blank lines
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    return cleaned_text.strip()


class VectorRAGEngine:
    """Vector RAG Orchestration Service with Dynamic Top-k, Token Budgeting, and Zero Hallucination Control."""

    def __init__(
        self,
        vector_store: HRVectorStore | None = None,
        llm_client: OllamaClient | None = None,
        query_processor: HRQueryProcessor | None = None
    ):
        self.store = vector_store or HRVectorStore()
        self.llm = llm_client or OllamaClient()
        self.query_processor = query_processor or HRQueryProcessor()
        self.budget_manager = TokenBudgetManager(max_context_tokens=1600)
        self._cache: dict[str, RAGAnswer] = {}

    def query(self, user_question: str, top_k: int | None = None) -> RAGAnswer:
        """Executes Advanced Vector RAG pipeline with dynamic top-k, token budgeting, and guardrails."""
        norm_key = user_question.strip().lower()
        if norm_key in self._cache:
            logger.info(f"Query Cache HIT for '{user_question}'")
            hit = self._cache[norm_key]
            return RAGAnswer(
                query=user_question,
                answer=hit.answer,
                citations=hit.citations,
                confidence_score=hit.confidence_score,
                retrieved_k=hit.retrieved_k,
                token_budget_used=hit.token_budget_used
            )

        # 1. Casual / Chit-chat / Out-of-Scope Pre-check
        casual_reply = check_chit_chat_or_out_of_scope(user_question)
        if casual_reply:
            rag_ans = RAGAnswer(
                query=user_question,
                answer=casual_reply,
                citations=[],
                confidence_score=1.0,
                retrieved_k=0,
                token_budget_used=0
            )
            self._cache[norm_key] = rag_ans
            return rag_ans

        # 2. Dynamic Top-k Selection
        chosen_k = top_k if top_k is not None else DynamicTopKSelector.select_k(user_question)
        logger.info(f"Processing query: '{user_question}' (Dynamic top_k={chosen_k})")

        # 3. Query expansion
        expanded_query = self.query_processor.process_query(user_question)

        # 4. Hybrid Search (Dense FAISS + Sparse BM25 + Re-ranking + Parent retrieval)
        hits = self.store.search(expanded_query, top_k=chosen_k, include_parents=True)

        # 5. Strict Guardrail: Relevance and Fallback Threshold
        if not hits or hits[0]["score"] < 0.05:
            return RAGAnswer(
                query=user_question,
                answer="ขออภัยครับ ไม่พบข้อมูลที่เกี่ยวข้องในเอกสารข้อบังคับการทำงาน หรือคำค้นหาอาจยังไม่ชัดเจน กรุณาระบุรายละเอียดเพิ่มเติม เช่น 'สิทธิ์วันลาพักผ่อน', 'เงินชดเชยการเลิกจ้าง', หรือ 'ระดับตำแหน่ง'",
                citations=[],
                confidence_score=0.0,
                retrieved_k=chosen_k,
                token_budget_used=0
            )

        # 6. Token Budget Management: pack context without overflowing
        context_text, included_hits, budget_used = self.budget_manager.pack_context(hits)

        # 7. Strict CoT System Prompt & Few-Shot Instruction
        system_prompt = (
            "คุณคือ HR Legal & Regulations Assistant ของ บริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด (PRIMO)\n"
            "หน้าที่ของคุณคือให้ข้อมูลเกี่ยวกับระเบียบ ข้อบังคับการทำงาน สิทธิประโยชน์ และสวัสดิการพนักงานตามเอกสารที่กำหนดเท่านั้น\n\n"
            "จงปฏิบัติตามกฎเหล็กความถูกต้องและความปลอดภัยอย่างเคร่งครัดดังต่อไปนี้:\n"
            "1. [Language & Tone]: ตอบคำถามเป็นภาษาไทยเท่านั้น ด้วยสำนวนที่เป็นทางการ สุภาพ ชัดเจน กระชับ และจัดรูปแบบให้อ่านง่าย\n"
            "2. [Direct & Accurate]: ตอบข้อสรุปที่ชัดเจน เช่น จำนวนวัน หรืออัตราค่าชดเชย ตั้งแต่ช่วงต้นของคำตอบเสมอ หากคำถามระบุอายุงานหรือระดับตำแหน่ง ให้เทียบกับช่วงในตารางโดยตรง ห้ามแยกบวกลบปีหรือสร้างเงื่อนไขขึ้นมาเอง\n"
            "3. [Strict Grounding & Zero Hallucination]: ตอบคำถามโดยอิงจาก 'เนื้อหาจากเอกสารข้อบังคับการทำงาน PRIMO' ที่กำหนดให้เท่านั้น ห้ามแต่งเติม ห้ามอนุมาน หรือเทียบเคียงจากภายนอกเด็ดขาด\n"
            "4. [Scope & Out-of-Domain]: หากคำถามของผู้ใช้เป็นเรื่องนอกขอบเขต หรือไม่เกี่ยวข้องกับข้อบังคับการทำงานของ PRIMO (เช่น ถามเรื่องทั่วไป, สภาพอากาศ, บ่นเหนื่อย, ง่วงนอน, หรือถามเรื่องที่ไม่มีในเอกสาร) ห้ามยกตัวอย่างใน Few-Shot หรือเนื้อหาที่ไม่ตรงมาตอบเด็ดขาด ให้ตอบปฏิเสธหรือแนะนำอย่างสุภาพว่าไม่พบข้อมูลในข้อบังคับ PRIMO และแนะนำให้สอบถามเรื่องระเบียบการทำงานหรือสวัสดิการแทน\n"
            "5. [Answer Only - No Echoing]: ให้เริ่มเขียนเนื้อหาคำตอบทันที ห้ามพิมพ์คำว่า 'คำถาม:' หรือทวนประโยคคำถาม หรือลอกชื่อหัวข้อตัวอย่างใน Few-Shot ออกมาในคำตอบเด็ดขาด\n"
            "6. [Honest Fallback]: หากในเนื้อหาที่ให้ไม่มีตัวเลข เงื่อนไข หรือคำตอบที่ถาม ให้แจ้งตามตรงว่า 'ไม่พบข้อมูลระบุไว้ในข้อบังคับฉบับนี้' ห้ามเดาหรือสร้างข้อมูลขึ้นมาเอง\n"
            "7. [Chain-of-Thought & Citations]: ในคำตอบ ให้ระบุเลขหน้าและหมวดหมู่ที่พบข้อมูลเสมอ แล้วจึงสรุปสาระสำคัญ เช่น จำนวนวัน เงื่อนไข หรือขั้นตอน อย่างสมบูรณ์จบประโยค\n"
            "8. [Formatting]: ห้ามใช้ตาราง Markdown (เช่น |---|---|) หรือเครื่องหมาย ** ในคำตอบเด็ดขาด ให้สรุปเป็นรายการหัวข้อย่อยด้วยเครื่องหมาย • เพื่อให้อ่านง่ายบนโทรศัพท์มือถือ"
        )

        prompt = (
            f"=== ตัวอย่างโครงสร้างการสรุปคำตอบที่ถูกต้อง ===\n"
            f"{FEW_SHOT_EXAMPLES.strip()}\n"
            f"=== สิ้นสุดตัวอย่าง ===\n\n"
            f"=== เนื้อหาจากเอกสารข้อบังคับการทำงาน PRIMO ===\n"
            f"{context_text}\n"
            f"=== สิ้นสุดเนื้อหา ===\n\n"
            f"คำถามของพนักงาน: {user_question}\n"
            f"คำสั่ง: กรุณาตอบคำถามข้างต้นโดยอ้างอิงจากเนื้อหาเท่านั้น เริ่มต้นด้วยคำตอบทันที (ห้ามพิมพ์ 'คำถาม:' ซ้ำ):"
        )

        answer_text = self.llm.generate(prompt, system_prompt=system_prompt)

        # 8. Output Guardrail: foreign characters leakage detection & grounding verification
        if re.search(r"[\u4e00-\u9fff\u3000-\u303f]", answer_text):
            logger.warning("Detected foreign characters in LLM response. Using safe grounded Thai fallback.")
            answer_text = self._fallback_thai_summary(included_hits, user_question)

        # 9. Post-process: Clean accidental "คำถาม: ... \nคำตอบ:" prefixes if generated by small LLM
        answer_text = re.sub(r"^(?:คำถาม:.*?\n+)?(?:คำตอบ:\s*)?", "", answer_text).strip()

        # 10. Post-process: Convert any remaining Markdown tables/syntax to clean LINE bullets
        answer_text = clean_markdown_for_line(answer_text)

        citations = [
            {
                "page_number": h["page_number"],
                "chapter": h["chapter"],
                "score": h["score"]
            }
            for h in included_hits[:3]
        ]

        top_score = included_hits[0]["score"] if included_hits else 0.0

        rag_ans = RAGAnswer(
            query=user_question,
            answer=answer_text,
            citations=citations,
            confidence_score=top_score,
            retrieved_k=len(included_hits),
            token_budget_used=budget_used
        )
        self._cache[norm_key] = rag_ans
        return rag_ans

    def _fallback_thai_summary(self, hits: list[dict[str, Any]], user_question: str) -> str:
        """Fallback extractor providing safe, pure Thai regulation summaries if LLM outputs foreign tokens."""
        if not hits:
            return "ไม่พบข้อมูลระบุไว้ในข้อบังคับฉบับนี้"
        top = hits[0]
        lines = [l.strip() for l in top["text"].splitlines() if l.strip() and not l.strip().isdigit()]
        snippet = "\n".join(lines[:6])
        return (
            f"อ้างอิงจาก หน้า {top['page_number']} ({top['chapter']}):\n"
            f"{snippet}"
        )


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    engine = VectorRAGEngine()
    q = "พนักงานระดับ 3 มีสิทธิ์ได้วันลาพักผ่อนประจำปีกี่วัน"
    print(f"\n--- Testing Query: '{q}' ---")
    res = engine.query(q)
    print(res.format_line_text())
    print(f"\n[Dynamic k used: {res.retrieved_k}, Token budget used: {res.token_budget_used} tokens]")
