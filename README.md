# 🤖 Sabai-Rules: LINE Chatbot (Vector RAG) & HR Document Knowledge Graph Analytics

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Neo4j 5.x](https://img.shields.io/badge/Neo4j-5.x-008CC1.svg)](https://neo4j.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ระบบสืบค้นสิทธิประโยชน์และวิเคราะห์ข้อบังคับเกี่ยวกับการทำงานอัจฉริยะ แบ่งสถาปัตยกรรมออกเป็น 2 ส่วนหลัก:

1. **LINE Chatbot (Pure Vector RAG):** สืบค้นข้อความจากเอกสาร PDF ฉบับเต็ม ตอบคำถามพนักงานผ่าน LINE Messaging API อย่างรวดเร็ว พร้อมอ้างอิงหมวดหมู่และเลขหน้า
2. **Knowledge Graph Analytics (Neo4j):** วิเคราะห์โครงสร้างและความสัมพันธ์ของข้อมูลในเอกสาร PDF เช่น ลำดับชั้นตำแหน่ง สิทธิวันลาข้ามระดับ เงื่อนไขอายุงาน และเครือข่ายระเบียบวินัย

*กรณีศึกษา: บริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด ในเครือ Origin Property (สกัดจากเอกสารข้อบังคับการทำงานฉบับเต็ม 47 หน้า)*

---

## 🌐 Language & Technical Documentation

- [🇹🇭 ภาษาไทย (Thai Documentation)](#-ภาษาไทย-thai-version)
- [🇬🇧 English Documentation](#-english-version)
- [📘 **เอกสารรวมสถาปัตยกรรมและรายงานโครงการฉบับสมบูรณ์ (Master Project Documentation)**](docs/master_documentation.md) 🌟 *(รวมเนื้อหาครบทุกมิติ ฉบับสมบูรณ์)*
- [📋 **สรุปสถาปัตยกรรมและเหตุผลการเลือกเครื่องมือตาม 6 รูบิค (Rubric Architecture Summary)**](docs/architecture_rubric_summary.md) ⭐ *(เจาะลึก 6 เกณฑ์, System Prompt, และ Ablation Study)*
- [🏛️ ผังและรายละเอียดสถาปัตยกรรมระบบทั้งระบบ (System Architecture &amp; Tech Stack)](docs/system_architecture.md)
- [📊 รายงานผลการประเมินเชิงปริมาณ RAG (Quantitative Evaluation Report)](docs/rag_evaluation_report.md)
- [🎙️ สคริปต์การนำเสนอโครงการ 5 นาที (5-Minute Presentation Script)](docs/presentation_script_5min.md)
- [🧪 คู่มือชุดคำถามทดสอบระบบ LINE Chatbot (Test Questions Guide)](docs/test_qa_guide.md)

---

# 🇹🇭 ภาษาไทย (Thai Version)

## 📌 1. ภาพรวมสถาปัตยกรรม 2 เสาหลัก (Two-Pillar Architecture)

```
[ เอกสารข้อบังคับการทำงาน PRIMO (PDF 47 หน้า) ]
       │                                           │
       ▼                                           ▼
[ เสาหลักที่ 1: Production-Grade Hybrid RAG ]     [ เสาหลักที่ 2: Knowledge Graph Analysis ]
 • PyMuPDF + PDFPlumber Layout/Table Ingestion     • Entity & Ontological Modeling
 • Small-to-Big Parent Document (373 Chunks)       • Multi-hop Relationship Discovery
 • Hybrid Search: FAISS (Dense) + BM25 (Sparse)    • Neo4j Graph Database
 • Reciprocal Rank Fusion (RRF) & Re-ranking       • Organizational Topology & Analytics
 • Dynamic Top-k (k=2..5) & Token Budgeting        • Disciplinary Network & Matrix Reports
 • Strict CoT & Zero Hallucination Guardrails
 • LINE Bot Webhook (FastAPI) & LIFF Calculator
```

### เสาหลักที่ 1: LINE Chatbot ด้วย Production-Grade Hybrid RAG

- **การสกัดและจัดโครงสร้าง:** สกัดข้อความและตารางด้วย PyMuPDF และ PDFPlumber (Noise < 5%) พร้อมใช้ **Small-to-Big Parent-Document Retrieval** (Child 250 / Parent 800+ ตัวอักษร) ผนวก 5 ตาราง Markdown คุณภาพสูง
- **เครื่องยนต์สืบค้นลูกผสม (Hybrid Search):** รวม **Dense Vector (FAISS IndexFlatIP bge-m3 1024d)** เข้ากับ **Sparse Lexical (BM25Okapi)** ผสานด้วย **Reciprocal Rank Fusion (RRF)** และตัดสัญญาณรบกวนด้วย **HRReranker**
- **การควบคุมบริบท:** ปรับค่า Top-k แบบไดนามิกด้วย **DynamicTopKSelector** (k=2 ถึง 5) และคุมขนาดบริบทด้วย **TokenBudgetManager** (1,600 tokens) ป้องกันปัญหา Context Overflow
- **การตอบกลับ:** โมเดล Local LLM (Ollama Qwen2.5) สังเคราะห์คำตอบด้วย **Strict Few-Shot Chain-of-Thought (CoT)**, มีระบบตรวจจับ Hallucination และแปลงตารางเป็น Mobile-Friendly Bullet points สวยงามบน **LINE Flex Message Bubble** พร้อมระบุเลขหน้าอ้างอิงชัดเจน
- **ความรวดเร็วและเครื่องคิดเลข:** ระบบ Asynchronous Background Worker ป้องกัน LINE 3s Timeout พร้อมมินิเว็บแอป **LIFF HR Calculator** คำนวณวันลา ค่าชดเชยเลิกจ้าง และเงินสะสม PVD ได้ในตัว

### เสาหลักที่ 2: Knowledge Graph วิเคราะห์ความสัมพันธ์ของข้อมูลใน PDF

- **การทำงาน:** สร้าง Ontology กราฟความสัมพันธ์บน Neo4j ครอบคลุมพนักงาน 9 ระดับ, สวัสดิการ 12 หมวด, และวันลา 7 ประเภท
- **การวิเคราะห์เชิงลึก:** สคริปต์ `src/graph/analytics.py` สำหรับวิเคราะห์:
  1. โครงสร้างลำดับชั้นตำแหน่ง (Job Level 1–9 vs Position Distribution)
  2. สิทธิ์วันลาพักผ่อนประจำปีตามระดับตำแหน่ง (Progression Matrix)
  3. เมทริกซ์เงื่อนไขการลาและเอกสารที่ต้องใช้ (Leave Policy Matrix)
  4. อัตราค่าชดเชยการเลิกจ้างตามอายุงาน (Severance Pay Schedule)
  5. โครงข่ายลำดับขั้นการลงโทษทางวินัย (Disciplinary Action Network)

---

## 📋 2. แผนงานและสถานะงาน (Project Roadmap & Task Checklist)

- [X] **Phase 1: Project Environment & Architecture Setup**
  - [X] โครงสร้างโฟลเดอร์แบบ Clean Architecture
  - [X] ติดตั้ง Python Virtual Environment (`.venv`)
  - [X] คอนฟิก `.env.example`, `requirements.txt`, `pytest.ini`, `Makefile`
- [X] **Phase 2: Knowledge Graph Relationship Analytics (สำหรับวิเคราะห์ข้อมูล PDF)**
  - [X] ออกแบบ Ontology Schema ครอบคลุมพนักงาน 9 ระดับ, สวัสดิการ 12 หมวด, วันลา 7 ประเภท
  - [X] สกัดข้อมูลกฎระเบียบเป็น Cypher Seeds (`data/knowledge_graph/primo_knowledge_graph.cypher`)
  - [X] พัฒนาระบบเชื่อมต่อ Neo4j Connection Pool (`src/graph/connection.py`, `src/graph/seeder.py`)
  - [X] พัฒนาเครื่องมือวิเคราะห์ความสัมพันธ์และสร้างรายงาน (`src/graph/analytics.py`, `src/graph/queries.py`)
- [X] **Phase 3: Vector Ingestion & Chunker (สำหรับ LINE Chatbot)**
  - [X] สกัดข้อความจาก PDF 47 หน้า ด้วย PyMuPDF พร้อมฟังก์ชัน Normalization ภาษาไทย (`src/vector/loader.py`)
  - [X] แบ่ง Chunk แบบ Section-aware รักษาบริบทภาษาไทย (212 Chunks) (`src/vector/chunker.py`)
  - [X] พัฒนาระบบจัดเก็บและสืบค้น Vector Store (`src/vector/store.py`)
- [X] **Phase 4: Vector RAG & Local LLM Orchestration**
  - [X] ตัวเชื่อมต่อ Local LLM Ollama (`src/llm/client.py`)
  - [X] Vector RAG Engine พร้อม Grounding Prompt และระบบอ้างอิงเลขหน้า (`src/rag/vector_rag.py`)
- [X] **Phase 5: FastAPI Webhook & LINE Bot Integration**
  - [X] FastAPI Server รองรับ Webhook `/callback`, `/health`, และ `/ask` (`src/webhook/server.py`)
  - [X] ระบบ Asynchronous Background Worker ป้องกัน LINE 3s Timeout (`src/webhook/line_handler.py`)
  - [X] ออกแบบ LINE Flex Message Bubble Cards แสดงผลสวยงาม
- [X] **Phase 6: Automated Testing & Verification Suite**
  - [X] ชุดทดสอบ Graph (`tests/test_graph.py`)
  - [X] ชุดทดสอบ Vector RAG และ API Endpoints (`tests/test_vector_rag.py`)

---

## 💻 3. วิธีการติดตั้งและเริ่มใช้งาน (Cross-Platform Setup Guide)

### 3.1 สิ่งที่ต้องเตรียม (Prerequisites)

- **Python 3.10 ขึ้นไป** (แนะนำ Python 3.11 หรือ 3.12)
- **Docker Desktop** (สำหรับรัน Neo4j Container) หรือ **Neo4j Desktop / Neo4j AuraDB**

---

### 3.2 ขั้นตอนสำหรับ Windows

#### การใช้ PowerShell:

```powershell
# 1. เข้าสู่โฟลเดอร์โปรเจค
cd d:\psu\AIE\4-1\241_351ModuleAIforSocialMedia\Assignment_2\sabai-rules

# 2. สร้าง Virtual Environment
python -m venv .venv

# 3. เปิดใช้งาน Virtual Environment
.\.venv\Scripts\Activate.ps1
# หากเจอนโยบายความปลอดภัย ให้รัน: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 4. ติดตั้ง Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. คัดลอกและตั้งค่า Environment Variables
Copy-Item .env.example .env
```

#### การใช้ Command Prompt (CMD):

```cmd
cd d:\psu\AIE\4-1\241_351ModuleAIforSocialMedia\Assignment_2\sabai-rules
python -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

---

### 3.3 ขั้นตอนสำหรับ macOS & Linux

```bash
# 1. เข้าสู่โฟลเดอร์โปรเจค
cd sabai-rules

# 2. สร้าง Virtual Environment
python3 -m venv .venv

# 3. เปิดใช้งาน Virtual Environment
source .venv/bin/activate

# 4. ติดตั้ง Dependencies
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# 5. คัดลอกและตั้งค่า Environment Variables
cp .env.example .env
```

---

## 🐳 4. การเปิดใช้งานฐานข้อมูล Neo4j

### ทางเลือกที่ 1: รันด้วย Docker Compose (แนะนำ)

```bash
docker compose up -d
```

- **Neo4j Browser (Web UI):** http://localhost:7474
- **Bolt Port:** `localhost:7687`
- **Username:** `neo4j`
- **Password:** `SecretPassword123`

### ทางเลือกที่ 2: ใช้ Container เดิมที่มีอยู่แล้ว

หากในเครื่องมีคอนเทนเนอร์ Neo4j กำลังรันอยู่แล้ว สามารถตรวจสอบและตั้งรหัสผ่านในไฟล์ `.env` ให้ตรงกัน:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=SecretPassword123
```

---

## 🚀 5. การรัน Knowledge Graph และตรวจสอบผล (Phase 1)

### 5.1 สั่ง Seed ข้อมูลข้อบังคับการทำงานลงสู่ Neo4j

```bash
# Windows
.\.venv\Scripts\python.exe -m src.graph.seeder

# macOS / Linux
python3 -m src.graph.seeder
```

*ระบบจะสร้าง Schema Constraints, Entity Labels และ Ingest Nodes & Relationships ทั้งหมด 100+ รายการจากเอกสาร 47 หน้า*

### 5.2 วิเคราะห์ความสัมพันธ์ของข้อมูลใน PDF (Knowledge Graph Relationship Analytics)

```bash
# รันการวิเคราะห์โครงสร้างองค์กร สิทธิวันลา ค่าชดเชย และบทลงโทษจาก Neo4j
python -m src.graph.analytics
# หรือ
make analytics
```

### 5.3 สกัด Entities ครบทั้ง 47 หน้า ด้วย Qwen2.5:7b (Hybrid Graph Extraction)

```bash
# สกัด Entities และความสัมพันธ์ทั้ง 12 หมวด 19 ส่วนย่อย ด้วย Qwen2.5:7b
make extract
# หรือ
python -m src.graph.llm_extractor

# นำเข้าข้อมูลที่สกัดใหม่ลง Neo4j (ล้างโหนดเดิมและ Seed ข้อมูลใหม่ครบ 47 หน้า)
python -m src.graph.seeder --reset

# ตรวจสอบผลการเชื่อมโยงความสัมพันธ์หลังสกัด
python -m src.graph.analytics
```

### 5.4 สร้าง Hybrid Vector & BM25 Index จาก PDF สำหรับ LINE Chatbot

```bash
# สกัด 47 หน้า แบ่ง Small-to-Big (373 Chunks, 52 Parents) และสร้าง FAISS + BM25Okapi Index บันทึกลง Disk
python -m src.vector.store
# หรือ
make ingest
```

### 5.5 ทดสอบระบบ Vector RAG ผ่าน Terminal

```bash
# ทดสอบถาม-ตอบสิทธิประโยชน์ด้วย Local LLM (Ollama)
python -m src.rag.vector_rag
# หรือ
make rag
```

### 5.6 เปิดใช้งาน FastAPI Webhook Server (LINE Chatbot)

```bash
# รัน Webhook Server ที่พอร์ต 8000
python -m src.webhook.server
# หรือ
make chatbot
```

- **Interactive Swagger Docs:** http://localhost:8000/docs
- **Health Check Endpoint:** http://localhost:8000/health
- **LINE Webhook Receiver:** `POST /callback`
- **Local Test Endpoint:** `POST /ask`

### 5.7 เชื่อมต่อภายนอกสู่ LINE ด้วย Cloudflare Tunnel (จำเป็นสำหรับการแชตผ่าน LINE)

เนื่องจาก LINE Messaging API ต้องยิง Webhook เข้าหา Public HTTPS URL เราจึงใช้ **Cloudflare Tunnel** เพื่อ Forward พอร์ต 8000 ออกสู่อินเทอร์เน็ต:

```bash
# 1. รัน Cloudflare Tunnel ชี้ไปที่พอร์ต 8000
cloudflared tunnel --url http://localhost:8000
```

**ขั้นตอนการนำ URL ไปผูกกับ LINE Developers Console:**

1. คัดลอก Public HTTPS URL ที่ได้จากหน้าจอ Terminal (เช่น `https://xxxx-xxxx.trycloudflare.com`)
2. เข้าสู่ [LINE Developers Console](https://developers.line.biz/) -> เลือก Channel ของคุณ -> แท็บ **Messaging API**
3. ในส่วน **Webhook settings**:
   - กรอก Webhook URL: `https://xxxx-xxxx.trycloudflare.com/callback` (ต้องต่อท้ายด้วย `/callback`)
   - เปิดสวิตช์ **Use webhook** ให้เป็น **ON**
   - กดปุ่ม **Verify** เพื่อทดสอบเชื่อมต่อ (ต้องขึ้นสถานะ `Success`)
4. ปิดการตอบกลับอัตโนมัติของ LINE (Auto-reply messages) ในหน้า LINE Official Account Manager เพื่อให้บอท AI ตอบเพียงตัวเดียว

### 5.8 รันการประเมินผลเชิงปริมาณ (Quantitative Evaluation Suite)

```bash
# รันชุดประเมิน 15 Q&A Pairs คำนวณ SBERT Cosine, BERTScore, Faithfulness และ Relevance
python -m scripts.evaluate_rag_metrics
# หรือ
make eval
```

### 5.9 รันชุดทดสอบอัตโนมัติ (Pytest Test Suite ครบ 15/15 รายการ)

```bash
pytest -v
# หรือ
make test
```

### 5.9 เอกสารและคู่มือการทดสอบระบบ (Documentation & Test Suite)

- 🧪 **[คู่มือชุดคำถามทดสอบระบบ LINE Chatbot (docs/test_qa_guide.md)](docs/test_qa_guide.md)**: รวบรวม 11 คำถามครอบคลุม 7 หมวดหมู่กฎหมายแรงงาน พร้อมเฉลยคำตอบที่ถูกต้อง หน้าอ้างอิง และตาราง Copy-Paste สำหรับทดสอบถามใน LINE
- 📊 **[รายงานผลการทดสอบเปรียบเทียบ Embedding Benchmark (docs/embedding_benchmark.md)](docs/embedding_benchmark.md)**: รายงานวิเคราะห์ประสิทธิภาพเชิงลึกระหว่าง `TF-IDF`, `all-minilm`, `nomic-embed-text` และ `bge-m3` พร้อมผลวัด MRR, Top-1, Top-3 และความเร็ว

### 5.10 การติดตั้ง Rich Menu และมินิเว็บแอป LIFF Calculator

```bash
# 1. สร้างภาพกราฟิก Rich Menu ขนาดมาตรฐาน LINE (2500 x 1686 พิกเซล)
python -m scripts.generate_richmenu_image

# 2. ลงทะเบียน Rich Menu 6 ช่องและตั้งเป็น Default บน LINE OA อัตโนมัติ
python -m scripts.setup_richmenu
```

- **URL เข้าใช้งาน Sabai HR Calculator:** `http://localhost:8000/liff/calculator` (หรือผ่าน Public URL ของ Cloudflare Tunnel: `https://<tunnel-domain>/liff/calculator`)
- **ความสามารถของ Calculator:** คำนวณวันลาพักร้อนสะสมตาม Job Level 1–9, คำนวณค่าชดเชยการเลิกจ้างตามอายุงาน (ม.118), และคำนวณเงินสมทบกองทุนสำรองเลี้ยงชีพ (PVD) พร้อมปุ่มแชร์สรุปลงห้องแชต LINE

---

## 📁 6. โครงสร้างโฟลเดอร์โปรเจค (Directory Structure)

```text
sabai-rules/
├── .env.example                     # ไฟล์แม่แบบ Environment Variables
├── requirements.txt                 # รายการ Dependencies ทั้งหมดของระบบ (Pinned Versions)
├── README.md                        # เอกสารอธิบายระบบ (TH/EN)
├── Dockerfile                       # Production Docker Container Specification
├── docker-compose.yml               # Container Orchestration (Neo4j & Sabai RAG)
├── Makefile                         # คำสั่งลัด (make eval, test, ingest, chatbot, etc.)
├── pytest.ini                       # การตั้งค่าทดสอบ Pytest
├── pyproject.toml                   # มาตรฐานบรรจุภัณฑ์ Python Packaging
├── data/
│   ├── ข้อบังคับเกี่ยวกับการทำงาน-PRIMO-Group (1).pdf # เอกสารต้นฉบับ 47 หน้า
│   ├── richmenu/                    # รูปภาพกราฟิก Rich Menu ขนาดมาตรฐาน LINE
│   ├── knowledge_graph/
│   │   ├── schema.cypher            # คำสั่งสร้าง Index & Unique Constraints
│   │   ├── primo_knowledge_graph.cypher # Cypher Seeds สกัดจาก PDF 47 หน้า (Core)
│   │   └── benefits_data.json       # ไฟล์ JSON สรุปกฎระเบียบและสิทธิประโยชน์
│   └── vector_store/                # ดัชนี Hybrid Store (สร้างอัตโนมัติด้วย make ingest)
│       ├── hr_faiss_bge-m3.index    # Dense Vector Index (1024d)
│       ├── hr_bm25.pkl              # Sparse BM25Okapi Model
│       ├── hr_chunks.json           # Small Child Chunks (373 Chunks)
│       └── hr_parents.json          # Big Parent Contexts (52 Parents)
├── docs/                            # รายงานการประเมินและเอกสารทางเทคนิค
│   ├── rag_evaluation_report.md     # รายงานผลประเมินเชิงปริมาณ SBERT/BERTScore/Faithfulness
│   ├── presentation_script_5min.md  # สคริปต์การนำเสนอโครงการ 5 นาที
│   ├── test_qa_guide.md             # คู่มือชุดคำถามทดสอบถาม-ตอบ
│   └── embedding_benchmark.md       # รายงาน Benchmark โมเดลเวกเตอร์
├── scripts/                         # สคริปต์ประเมินผลและยูทิลิตี้
│   ├── evaluate_rag_metrics.py      # Quantitative Evaluation Suite (15 Q&A Pairs)
│   ├── benchmark_embeddings.py      # Empirical Vector Search Benchmark
│   ├── generate_richmenu_image.py   # สร้างกราฟิก Rich Menu
│   └── setup_richmenu.py            # อัปโหลดและเปิดใช้งาน Rich Menu บน LINE OA
├── src/
│   ├── config.py                    # โหลดการตั้งค่าด้วย Pydantic Settings
│   ├── graph/                       # Pillar 2: Knowledge Graph Analysis Engine
│   │   ├── connection.py            # Neo4j Driver Connection Pool
│   │   ├── seeder.py                # สคริปต์รัน Seed ข้อมูลลงกราฟ (รองรับ --reset)
│   │   ├── queries.py               # Deterministic Cypher Query Service
│   │   ├── verify_graph.py          # สคริปต์ตรวจสอบความถูกต้องของโหนด
│   │   └── analytics.py             # เอนจินวิเคราะห์ความสัมพันธ์และสร้างรายงาน
│   ├── vector/                      # Pillar 1: Document Processing & Vector Storage
│   │   ├── loader.py                # ตัวโหลด PDF (PyMuPDF + PDFPlumber ตรวจจับตาราง)
│   │   ├── chunker.py               # Small-to-Big Chunker + 5 ตาราง Markdown
│   │   ├── embeddings.py            # BGE-M3 Dense Embedding Client (Ollama)
│   │   ├── query_processor.py       # Synonym Expansion & HyDE Engine
│   │   ├── reranker.py              # Cross-Encoder & Salient Entity Re-ranker
│   │   └── store.py                 # Hybrid Retrieval (FAISS + BM25 + RRF Fusion)
│   ├── llm/                         # Local LLM Integration
│   │   └── client.py                # Ollama Client (/api/chat) พร้อม Safe Fallback
│   ├── rag/                         # Vector RAG Orchestration
│   │   └── vector_rag.py            # Dynamic Top-k, Token Budgeting, Strict CoT & Guardrails
│   └── webhook/                     # FastAPI & LINE Bot Integration
│       ├── server.py                # FastAPI Server (Webhook, Health, LIFF Calculator)
│       ├── flex_templates.py        # เทมเพลต LINE Flex Carousel, FAQ & Calculator
│       └── line_handler.py          # LINE Webhook Event Processor & Auto-Tunnel Resolve
└── tests/
    ├── test_line_ux.py              # ชุดทดสอบ Quick Replies, Flex Cards, LIFF Calculator
    ├── test_vector_rag.py           # ชุดทดสอบ Hybrid RAG, Dynamic Top-k & Token Budgeting
    └── test_graph.py                # ชุดทดสอบ Knowledge Graph
```

---

---

# 🇬🇧 English Version

## 📌 1. Project Overview

Enterprise employee benefit policies and working regulations are intrinsically multi-dimensional and complex. In particular, the **Primo Service Solution Co., Ltd. Working Regulations (47 pages)** define entitlements contingent upon:

1. **Hierarchy Level (Levels 1–9):** Annual leave entitlements scale from 6 days (L1-2), 7 days (L3-5), 8 days (L6-8), to 10 days (L9).
2. **Tenure Duration:** Provident Fund (PVD) matching requires 0% (< 1 yr), 50% (1-3 yrs), 100% (> 3 yrs). Statutory severance ranges from 30 to 300 days of wage.
3. **Probationary Status:** Group health insurance and dental subsidies are strictly reserved for post-probation employees.
4. **Employee Classification:** Overtime (OT) pay is statutory for operational staff, but strictly exempted for Department Managers and above (Level 4+).

### Why Hybrid GraphRAG?

- **Vanilla Vector RAG Limitation:** Chunking text across arbitrary boundaries breaks tabular structures and frequently causes numerical or role-swapping **hallucinations**.
- **Knowledge Graph (Neo4j):** Enforces **100% deterministic precision** on numerical policies, allowances, and multi-hop organizational hierarchies.
- **FAISS Vector Store:** Handles narrative descriptions, ethical guidelines, and legal workflows.
- **Local LLM (Ollama / Qwen2.5):** Synthesizes grounded natural language responses while ensuring enterprise **Zero Data Egress** privacy.

---

## 📋 2. Project Roadmap & Checklist

- [X] **Phase 1: Project Environment & Architecture Setup**
  - [X] Clean architecture directory layout
  - [X] Python virtual environment (`.venv`) isolation
  - [X] Configuration files (`.env.example`, `requirements.txt`, `pytest.ini`, `pyproject.toml`)
  - [X] Portable `docker-compose.yml` for Neo4j 5.x with APOC and Ollama
  - [X] Comprehensive bilingual `README.md` (TH/EN)
- [X] **Phase 2: Knowledge Graph Engineering**
  - [X] Knowledge Graph Ontology Schema (9 Levels, 12 Benefits, 7 Leave categories)
  - [X] Cypher seed definitions extracted from 47-page PDF (`primo_knowledge_graph.cypher`)
  - [X] Schema uniqueness constraints & traversal indexes (`schema.cypher`)
  - [X] Robust Neo4j connection pool manager (`src/graph/connection.py`)
  - [X] Automated graph seeder CLI (`src/graph/seeder.py`)
  - [X] Production multi-hop Cypher query service (`src/graph/queries.py`)
  - [X] Automated verification suite & Pytest coverage (`src/graph/verify_graph.py`, `tests/test_graph.py`)
- [X] **Phase 3: Vector Store & Ingestion (Production-Grade)**
  - [X] PDF text extraction with PyMuPDF (`fitz`) and PDFPlumber table parser
  - [X] Small-to-Big section-aware chunking (373 chunks) preserving Thai markdown tables
  - [X] High-performance FAISS index with `bge-m3` embedding model & BM25Okapi sparse index
- [X] **Phase 4: Hybrid RAG & Ollama LLM Orchestration**
  - [X] Hybrid Search (FAISS Dense + BM25 Sparse with Reciprocal Rank Fusion RRF)
  - [X] Query expansion (Thai HR synonyms/acronyms) & HyDE (Hypothetical Document Embeddings)
  - [X] Cross-Encoder Re-ranking with Salient Entity matching
  - [X] Dynamic Top-k (k=2..5) & Strict Token Budgeting (1,600 tokens)
  - [X] Grounded anti-hallucination Strict CoT prompt templates with Page Citations
  - [X] Mobile-optimized formatting (`clean_markdown_for_line`)
- [X] **Phase 5: FastAPI Webhook & LINE Bot Integration**
  - [X] FastAPI webhook endpoint with signature verification
  - [X] Asynchronous background tasks preventing LINE 3s timeout
  - [X] Interactive LINE Flex Message card carousel, Quick Replies, and LIFF Calculator
  - [X] Cloudflare Tunnel ingress configuration guide
- [X] **Phase 6: Automated Verification & Quantitative Evaluation Suite**
  - [X] Full test coverage for Vector RAG pipeline, LINE UX, and FastAPI endpoints
  - [X] Automated RAG Triad Evaluation Suite (`scripts/evaluate_rag_metrics.py`)
  - [X] Comprehensive reports: [System Architecture Blueprint](docs/system_architecture.md), [RAG Evaluation Report](docs/rag_evaluation_report.md) & [5-Min Presentation Script](docs/presentation_script_5min.md)

---

## 💻 3. Cross-Platform Setup Instructions

### 3.1 Prerequisites

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **Docker Desktop** (for running local Neo4j container) or native Neo4j instance
- **Ollama** with `bge-m3` and `qwen2.5:3b` models installed

---

### 3.2 Setup on Windows

#### PowerShell:

```powershell
cd d:\psu\AIE\4-1\241_351ModuleAIforSocialMedia\Assignment_2\sabai-rules
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

#### Command Prompt (CMD):

```cmd
cd d:\psu\AIE\4-1\241_351ModuleAIforSocialMedia\Assignment_2\sabai-rules
python -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

---

### 3.3 Setup on macOS & Linux

```bash
cd sabai-rules
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

---

## 🐳 4. Neo4j Database Setup

### Option 1: Docker Compose (Recommended)

```bash
docker compose up -d
```

- **Neo4j Browser:** http://localhost:7474
- **Bolt Protocol:** `bolt://localhost:7687`
- **Username:** `neo4j`
- **Password:** `SecretPassword123`

### Option 2: Existing Neo4j Instance

Update `.env` with your active Neo4j connection details:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=SecretPassword123
```

---

## 🚀 5. Execution Guide

### 5.1 Ingest PDF & Build Small-to-Big Hybrid Index

```bash
python -m src.vector.loader
```

### 5.2 Seed Knowledge Graph into Neo4j

```bash
python -m src.graph.seeder
```

### 5.3 Run Automated Unit Tests (Pytest)

```bash
pytest -v
```

### 5.4 Run Quantitative RAG Evaluation Benchmark

```bash
python scripts/evaluate_rag_metrics.py
```

### 5.5 Start FastAPI Webhook Server

```bash
python -m src.webhook.server
```

### 5.6 Connect to LINE via Cloudflare Tunnel

```bash
# Expose port 8000 via Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8000
```

- Copy the generated URL (`https://<subdomain>.trycloudflare.com/callback`) to your **LINE Developers Console** -> **Messaging API** -> **Webhook settings**.
- Enable **Use Webhook** and click **Verify**.

---

## 📄 7. License & Academic Attribution

Developed for **241-351 Module AI for Social Media**, Department of Artificial Intelligence Engineering (AIE), Prince of Songkla University. Released under the MIT License.
