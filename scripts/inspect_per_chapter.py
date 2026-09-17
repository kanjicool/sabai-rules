"""Extract per-chapter node connections for documentation."""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from src.graph.connection import Neo4jConnection

def run():
    conn = Neo4jConnection()
    with conn.session() as s:
        for c_num in range(1, 13):
            chap_q = "MATCH (c:Chapter {chapter_number: $c_num}) RETURN c.title_th AS title"
            res = s.run(chap_q, {"c_num": c_num}).single()
            if not res:
                continue
            title = res["title"]
            print(f"=== CHAPTER {c_num}: {title} ===")
            
            # Articles
            arts = s.run("MATCH (c:Chapter {chapter_number: $c_num})-[:CONTAINS_ARTICLE]->(a:Article) RETURN a.number AS num, a.title AS title, a.summary AS summary", {"c_num": c_num}).data()
            print(f"  Articles ({len(arts)}):")
            for a in arts:
                print(f"    - มาตรา {a['num']}: {a['title']} -> {a['summary'][:60]}...")
            
            # Misconducts & Penalties
            miscs = s.run("""
                MATCH (c:Chapter {chapter_number: $c_num})-[:DEFINES_MISCONDUCT]->(m:Misconduct)
                OPTIONAL MATCH (m)-[:SUBJECT_TO]->(p:DisciplinaryPenalty)
                RETURN m.name_th AS name, m.severity AS sev, p.level AS p_level, p.name AS p_name
            """, {"c_num": c_num}).data()
            print(f"  Misconducts ({len(miscs)}):")
            for m in miscs:
                p_desc = f"ขั้นที่ {m['p_level']} ({m['p_name']})" if m['p_level'] else "ไม่มีบทลงโทษ"
                print(f"    - [{m['sev']}] {m['name']} ---> SUBJECT_TO ---> {p_desc}")
            
            # Procedures
            procs = s.run("""
                MATCH (c:Chapter {chapter_number: $c_num})-[:HAS_STEP]->(pr:ProcedureStep)
                RETURN pr.step_number AS step, pr.action AS action, pr.timeline_days AS days, pr.responsible AS resp
                ORDER BY pr.step_number
            """, {"c_num": c_num}).data()
            print(f"  Procedures ({len(procs)}):")
            for pr in procs:
                days_txt = f"{pr['days']} วัน" if pr['days'] else "ไม่ระบุกรอบเวลา"
                print(f"    - ขั้นที่ {pr['step']}: {pr['action'][:50]}... (เวลา: {days_txt}, ผู้รับผิดชอบ: {pr['resp']})")
            
            # Exceptions
            excs = s.run("""
                MATCH (c:Chapter {chapter_number: $c_num})-[:HAS_EXCEPTION]->(ex:LegalException)
                RETURN ex.name AS name, ex.description AS desc
            """, {"c_num": c_num}).data()
            print(f"  Exceptions ({len(excs)}):")
            for e in excs:
                print(f"    - {e['name']}: {e['desc'][:60]}...")
            print()

if __name__ == "__main__":
    run()
