# 🤖 Sabai-Rules: LINE Chatbot HR Benefit Hybrid GraphRAG

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Neo4j 5.x](https://img.shields.io/badge/Neo4j-5.x-008CC1.svg)](https://neo4j.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ระบบสืบค้นสิทธิประโยชน์และข้อบังคับเกี่ยวกับการทำงานอัจฉริยะผ่าน LINE Chatbot ด้วยสถาปัตยกรรม **Hybrid GraphRAG (Neo4j + FAISS + Local LLM)**  
*กรณีศึกษา: บริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด ในเครือ Origin Property (สกัดจากเอกสารข้อบังคับการทำงานฉบับเต็ม 47 หน้า)*

---

## 🌐 Language Navigation / เลือกภาษา
- [🇹🇭 ภาษาไทย (Thai Documentation)](#-ภาษาไทย-thai-version)
- [🇬🇧 English Documentation](#-english-version)

---

# 🇹🇭 ภาษาไทย (Thai Version)

## 📌 1. ภาพรวมโปรเจค (Project Overview)
เอกสารระเบียบข้อบังคับการทำงานและสวัสดิการของพนักงานในองค์กรขนาดใหญ่มีความซับซ้อนสูง โดยเฉพาะข้อบังคับของ **บริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด (47 หน้า)** ซึ่งมีเงื่อนไขผูกพันหลายมิติ เช่น:
1. **มิติตำแหน่ง (Job Level 1–9):** เช่น สิทธิ์วันลาพักผ่อนประจำปี (Level 1–2 ได้ 6 วัน, Level 3–5 ได้ 7 วัน, Level 6–8 ได้ 8 วัน, Level 9 ได้ 10 วัน)
2. **มิติอายุงาน (Tenure):** เงินสมทบกองทุนสำรองเลี้ยงชีพ (PVD) จ่ายสมทบ 0% (< 1 ปี), 50% (1-3 ปี), 100% (> 3 ปี) และอัตราค่าชดเชยตามกฎหมายแรงงาน (30 ถึง 300 วัน)
3. **มิติสถานะทดลองงาน:** สิทธิ์ประกันสุขภาพกลุ่มและค่าทันตกรรม (จำกัดเฉพาะพนักงานที่ผ่านทดลองงานแล้ว)
4. **มิติประเภทพนักงาน:** สิทธิ์การเบิกค่าล่วงเวลา (OT) ยกเว้นพนักงานระดับผู้จัดการขึ้นไป (Level 4+)

### ทำไมต้องใช้ Hybrid GraphRAG?
- **Vector Search เดี่ยวๆ (Vanilla RAG):** มักพบปัญหาตัด Chunking ขาดบริบทตาราง และเสี่ยงต่อการเกิด **Hallucination** เรื่องตัวเลขและระดับตำแหน่ง (เช่น จำสับสนระหว่าง Senior และ Manager)
- **Knowledge Graph (Neo4j):** ล็อกตัวเลข กฎเกณฑ์ และความสัมพันธ์ให้ถูกต้อง **100% Deterministic** รองรับการสืบค้นแบบ Multi-hop Reasoning
- **FAISS Vector Store:** เก็บเนื้อหาข้อความบรรยาย ขั้นตอนการปฏิบัติ และบริบทกฎหมาย
- **Local LLM (Ollama / Qwen2.5):** สังเคราะห์คำตอบภาษาไทยได้อย่างเป็นธรรมชาติ รักษาความลับข้อมูลภายในองค์กร 100% (Zero Data Egress)

---

## 📋 2. แผนงานและสถานะงาน (Project Roadmap & Task Checklist)

- [x] **Phase 1: Project Environment & Architecture Setup**
  - [x] สร้างโครงสร้างโฟลเดอร์แบบ Clean Architecture
  - [x] ติดตั้ง Python Virtual Environment (`.venv`)
  - [x] สร้างไฟล์คอนฟิก `.env.example`, `requirements.txt`, `pytest.ini`, `pyproject.toml`
  - [x] จัดเตรียม `docker-compose.yml` สำหรับ Neo4j 5.x พร้อม APOC
  - [x] จัดทำคู่มือ `README.md` รองรับทุก OS (TH/EN)
- [x] **Phase 2: Knowledge Graph Engineering (โฟกัสหลักเฟสปัจจุบัน)**
  - [x] ออกแบบ Ontology Schema ครอบคลุมพนักงาน 9 ระดับ, สวัสดิการ 12 หมวด, วันลา 7 ประเภท
  - [x] สกัดข้อมูลกฎระเบียบจาก PDF 47 หน้า เป็น Cypher Seeds (`primo_knowledge_graph.cypher`)
  - [x] สร้าง Schema Constraints & Indexes (`schema.cypher`)
  - [x] พัฒนาระบบเชื่อมต่อ Neo4j Connection Pool (`src/graph/connection.py`)
  - [x] พัฒนาตัวรัน Seed ข้อมูลอัตโนมัติ (`src/graph/seeder.py`)
  - [x] พัฒนา Service สืบค้นกราฟแบบ Multi-hop (`src/graph/queries.py`)
  - [x] พัฒนาชุดทดสอบและสคริปต์ตรวจสอบความถูกต้อง (`src/graph/verify_graph.py`, `tests/test_graph.py`)
- [ ] **Phase 3: Document Chunking & FAISS Vector Ingestion (ขั้นตอนถัดไป)**
  - [ ] สกัดข้อความจาก PDF 47 หน้า ด้วย PyMuPDF (`fitz`)
  - [ ] แบ่ง Chunk ตามหมวดหมู่และรักษาโครงสร้างตาราง
  - [ ] สร้าง Vector Index ด้วย `paraphrase-multilingual-MiniLM-L12-v2`
- [ ] **Phase 4: Hybrid RAG & Ollama LLM Orchestration**
  - [ ] ตัวจัดเส้นทางคำถาม (Intent Classifier & Entity Extractor)
  - [ ] ผสานข้อมูลจาก Neo4j และ FAISS (Context Synthesizer)
  - [ ] ออกแบบ Anti-Hallucination Grounding Prompt อ้างอิงเลขหน้าและหมวดหมู่
- [ ] **Phase 5: FastAPI Webhook & LINE Bot Integration**
  - [ ] FastAPI Server รับ Webhook จาก LINE Platform
  - [ ] ระบบ Asynchronous Background Worker ป้องกัน LINE 3s Timeout
  - [ ] ออกแบบ LINE Flex Message Cards แสดงผลสิทธิประโยชน์แบบสวยงาม
  - [ ] ติดตั้ง Cloudflare Tunnel เพื่อเปิด Public HTTPS Webhook

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

### 5.2 รันสคริปต์ตรวจสอบความถูกต้อง (Interactive Verification)
```bash
# Windows
.\.venv\Scripts\python.exe -m src.graph.verify_graph

# macOS / Linux
python3 -m src.graph.verify_graph
```
*จะแสดงผลตารางเปรียบเทียบสิทธิประโยชน์ระดับ Operation, Senior, Manager, VP, CEO, กองทุน PVD, ค่าชดเชยตามอายุงาน และเอกสารที่ต้องใช้ในการลาแต่ละประเภท*

### 5.3 รันชุดทดสอบ Automated Tests (Pytest)
```bash
# Windows
.\.venv\Scripts\pytest -v

# macOS / Linux
pytest -v
```

---

## 📁 6. โครงสร้างโฟลเดอร์โปรเจค (Directory Structure)

```text
sabai-rules/
├── .env.example                     # ไฟล์แม่แบบ Environment Variables
├── requirements.txt                 # รายการ Dependencies ทั้งหมดของระบบ
├── README.md                        # เอกสารอธิบายระบบ (TH/EN)
├── docker-compose.yml               # การตั้งค่า Docker สำหรับ Neo4j
├── Makefile                         # คำสั่งลัดสำหรับ macOS / Linux
├── pytest.ini                       # การตั้งค่าทดสอบ Pytest
├── pyproject.toml                   # มาตรฐานบรรจุภัณฑ์ Python Packaging
├── data/
│   ├── ข้อบังคับเกี่ยวกับการทำงาน-PRIMO-Group (1).pdf # เอกสารต้นฉบับ 47 หน้า
│   └── knowledge_graph/
│       ├── schema.cypher            # คำสั่งสร้าง Index & Unique Constraints
│       ├── primo_knowledge_graph.cypher # Cypher Seeds สกัดจาก PDF 47 หน้า
│       └── benefits_data.json       # ไฟล์ JSON สรุปกฎระเบียบและสิทธิประโยชน์
├── src/
│   ├── config.py                    # โหลดการตั้งค่าด้วย Pydantic Settings
│   ├── graph/                       # Knowledge Graph Engine (Phase 1 Focus)
│   │   ├── connection.py            # Neo4j Driver Connection Pool & Contexts
│   │   ├── seeder.py                # สคริปต์รัน Seed ข้อมูลลงกราฟ
│   │   ├── queries.py               # Cypher Multi-hop Service สำหรับ RAG
│   │   └── verify_graph.py          # สคริปต์แสดงผลตารางตรวจสอบความถูกต้อง
│   ├── vector/                      # Text Chunking & FAISS Vector Index (Phase 2)
│   ├── llm/                         # Ollama & Anti-Hallucination Prompts (Phase 3)
│   ├── rag/                         # Hybrid RAG Context Synthesizer (Phase 3)
│   └── webhook/                     # FastAPI & LINE Messaging Webhook (Phase 4)
└── tests/
    └── test_graph.py                # ชุดทดสอบ Unit Test สำหรับ Knowledge Graph
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

- [x] **Phase 1: Project Environment & Architecture Setup**
  - [x] Clean architecture directory layout
  - [x] Python virtual environment (`.venv`) isolation
  - [x] Configuration files (`.env.example`, `requirements.txt`, `pytest.ini`, `pyproject.toml`)
  - [x] Portable `docker-compose.yml` for Neo4j 5.x with APOC
  - [x] Comprehensive bilingual `README.md` (TH/EN)
- [x] **Phase 2: Knowledge Graph Engineering (Current Execution Focus)**
  - [x] Knowledge Graph Ontology Schema (9 Levels, 12 Benefits, 7 Leave categories)
  - [x] Cypher seed definitions extracted from 47-page PDF (`primo_knowledge_graph.cypher`)
  - [x] Schema uniqueness constraints & traversal indexes (`schema.cypher`)
  - [x] Robust Neo4j connection pool manager (`src/graph/connection.py`)
  - [x] Automated graph seeder CLI (`src/graph/seeder.py`)
  - [x] Production multi-hop Cypher query service (`src/graph/queries.py`)
  - [x] Automated verification suite & Pytest coverage (`src/graph/verify_graph.py`, `tests/test_graph.py`)
- [ ] **Phase 3: Vector Store & Ingestion (Upcoming Phase)**
  - [ ] PDF text extraction with PyMuPDF (`fitz`)
  - [ ] Section-aware chunking preserving Thai table context
  - [ ] FAISS vector index with `paraphrase-multilingual-MiniLM-L12-v2`
- [ ] **Phase 4: Hybrid RAG & Ollama LLM Orchestration**
  - [ ] Query intent classifier & entity extractor
  - [ ] Dual-retriever coordinator (Neo4j + FAISS)
  - [ ] Grounded anti-hallucination prompt templates with page citations
- [ ] **Phase 5: FastAPI Webhook & LINE Bot Integration**
  - [ ] FastAPI webhook endpoint with signature verification
  - [ ] Asynchronous background tasks preventing LINE 3s timeout
  - [ ] Interactive LINE Flex Message card renderer
  - [ ] Cloudflare Tunnel ingress configuration

---

## 💻 3. Cross-Platform Setup Instructions

### 3.1 Prerequisites
- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **Docker Desktop** (for running local Neo4j container) or native Neo4j instance

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

## 🚀 5. Running Knowledge Graph & Verifications (Phase 1)

### 5.1 Seed Knowledge Graph into Neo4j
```bash
# Windows
.\.venv\Scripts\python.exe -m src.graph.seeder

# macOS / Linux
python3 -m src.graph.seeder
```

### 5.2 Run Verification Suite
```bash
# Windows
.\.venv\Scripts\python.exe -m src.graph.verify_graph

# macOS / Linux
python3 -m src.graph.verify_graph
```

### 5.3 Execute Automated Unit Tests (Pytest)
```bash
# Windows
.\.venv\Scripts\pytest -v

# macOS / Linux
pytest -v
```

---

## 📄 7. License & Academic Attribution
Developed for **241-351 Module AI for Social Media**, Department of Artificial Intelligence Engineering (AIE), Prince of Songkla University. Released under the MIT License.