"""Script to thoroughly inspect and validate the generated Knowledge Graph from primo_hybrid_extracted.cypher."""

import sys
from collections import Counter
from pathlib import Path
from tabulate import tabulate

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from src.graph.connection import Neo4jConnection
from src.config import settings

def inspect():
    cypher_file = settings.KG_DIR / "primo_hybrid_extracted.cypher"
    if not cypher_file.exists():
        print(f"[ERROR] File not found: {cypher_file}")
        return

    content = cypher_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    print(f"📄 ตรวจสอบไฟล์: {cypher_file.name}")
    print(f"   ขนาดไฟล์: {len(content):,} bytes | จำนวนบรรทัด: {len(lines):,} บรรทัด\n")

    # 1. Inspect statements in Cypher file
    statement_types = Counter()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if "MERGE (chap" in stripped:
            statement_types["Chapter Node"] += 1
        elif "MERGE (a:Article" in stripped:
            statement_types["Article Node"] += 1
        elif "MERGE (m:Misconduct" in stripped:
            statement_types["Misconduct Node"] += 1
        elif "MERGE (pr:ProcedureStep" in stripped:
            statement_types["ProcedureStep Node"] += 1
        elif "MERGE (ex:LegalException" in stripped:
            statement_types["LegalException Node"] += 1
        elif "-[:SUBJECT_TO]->" in stripped:
            statement_types["Penalty Relation [:SUBJECT_TO]"] += 1
        elif "-[:DEFINES_MISCONDUCT]->" in stripped:
            statement_types["Misconduct Relation [:DEFINES_MISCONDUCT]"] += 1
        elif "-[:HAS_STEP]->" in stripped:
            statement_types["Procedure Relation [:HAS_STEP]"] += 1
        elif "-[:HAS_EXCEPTION]->" in stripped:
            statement_types["Exception Relation [:HAS_EXCEPTION]"] += 1
        elif "-[:CONTAINS_ARTICLE]->" in stripped:
            statement_types["Article Relation [:CONTAINS_ARTICLE]"] += 1

    print("📊 สรุปคำสั่ง Cypher ที่สกัดได้ในไฟล์:")
    table_stmts = [[k, v] for k, v in statement_types.items()]
    print(tabulate(table_stmts, headers=["ประเภท Entity / Relationship", "จำนวนคำสั่ง"], tablefmt="github"))

    # 2. Inspect Neo4j Live Database
    conn = Neo4jConnection()
    with conn.session() as s:
        total_nodes = s.run("MATCH (n) RETURN count(n) AS cnt").single()["cnt"]
        total_rels = s.run("MATCH ()-[r]->() RETURN count(r) AS cnt").single()["cnt"]
        labels = [r["label"] for r in s.run("CALL db.labels() YIELD label RETURN label")]
        rel_types = [r["relationshipType"] for r in s.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")]

        print(f"\n🌐 สถิติสดใน Neo4j Database หลังนำเข้า:")
        print(f"   • โหนดทั้งหมด (Total Nodes): {total_nodes}")
        print(f"   • ความสัมพันธ์ทั้งหมด (Total Relationships): {total_rels}")
        print(f"   • จำนวน Entity Labels: {len(labels)} ชนิด")
        print(f"   • จำนวน Relationship Types: {len(rel_types)} ชนิด\n")

        # 3. Chapter Coverage
        query_chap = """
        MATCH (c:Chapter)
        OPTIONAL MATCH (c)-[:CONTAINS_ARTICLE]->(a:Article)
        OPTIONAL MATCH (c)-[:DEFINES_MISCONDUCT]->(m:Misconduct)
        OPTIONAL MATCH (c)-[:HAS_STEP]->(p:ProcedureStep)
        OPTIONAL MATCH (c)-[:HAS_EXCEPTION]->(e:LegalException)
        RETURN c.chapter_number AS chap_num, c.title_th AS title,
               count(DISTINCT a) AS articles,
               count(DISTINCT m) AS misconducts,
               count(DISTINCT p) AS procedures,
               count(DISTINCT e) AS exceptions
        ORDER BY chap_num
        """
        chap_data = s.run(query_chap).data()
        chap_table = []
        for ch in chap_data:
            chap_table.append([
                f"หมวด {ch['chap_num']}",
                ch['title'],
                ch['articles'],
                ch['misconducts'],
                ch['procedures'],
                ch['exceptions']
            ])
        print("📑 ความครอบคลุมรายหมวด (Chapter Coverage):")
        print(tabulate(chap_table, headers=["หมวด", "ชื่อหมวด", "Articles", "Misconducts", "Procedures", "Exceptions"], tablefmt="github"))

        # 4. Check Disciplinary Linkages
        query_pen = """
        MATCH (p:DisciplinaryPenalty)
        OPTIONAL MATCH (m:Misconduct)-[:SUBJECT_TO]->(p)
        RETURN p.level AS level, p.name_th AS penalty, count(m) AS linked_misconducts
        ORDER BY level
        """
        pen_data = s.run(query_pen).data()
        pen_table = [[f"ขั้นที่ {r['level']}", r['penalty'], r['linked_misconducts']] for r in pen_data]
        print("\n⚖️ การเชื่อมโยงระดับบทลงโทษ (Penalty Links):")
        print(tabulate(pen_table, headers=["ระดับ", "มาตรการลงโทษ", "ความผิดที่ผูกมัด (ข้อ)"], tablefmt="github"))

        # 5. Check Sample Entities Quality
        sample_misconducts = s.run("MATCH (m:Misconduct) RETURN m.name_th AS name, m.severity AS sev, m.chapter AS chap LIMIT 5").data()
        print("\n🔍 ตัวอย่างความผิดวินัยที่สกัดได้ (Sample Misconducts):")
        for idx, m in enumerate(sample_misconducts, 1):
            print(f"   {idx}. [หมวด {m['chap']}] {m['name']} (ความร้ายแรง: {m['sev']})")

        sample_exceptions = s.run("MATCH (e:LegalException) RETURN e.name AS name, e.description AS desc LIMIT 4").data()
        print("\n🛡️ ตัวอย่างข้อยกเว้นทางกฎหมายที่สกัดได้ (Sample Legal Exceptions):")
        for idx, e in enumerate(sample_exceptions, 1):
            print(f"   {idx}. {e['name']}: {e['desc'][:70]}...")

if __name__ == "__main__":
    inspect()
