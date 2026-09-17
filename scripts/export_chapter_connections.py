"""Export full per-chapter connection breakdown to markdown."""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from src.graph.connection import Neo4jConnection

def export_markdown():
    conn = Neo4jConnection()
    output_lines = []
    
    with conn.session() as s:
        for c_num in range(1, 13):
            res = s.run("MATCH (c:Chapter {chapter_number: $c_num}) RETURN c.title_th AS title", {"c_num": c_num}).single()
            if not res:
                continue
            title = res["title"]
            output_lines.append(f"### หมวดที่ {c_num}: {title}\n")
            
            # Articles
            arts = s.run("MATCH (c:Chapter {chapter_number: $c_num})-[:CONTAINS_ARTICLE]->(a:Article) RETURN a.number AS num, a.title AS title, a.summary AS summary ORDER BY a.number", {"c_num": c_num}).data()
            if arts:
                output_lines.append(f"**1. มาตราและข้อบังคับ (`:Article`) เชื่อมโยงด้วย `[:CONTAINS_ARTICLE]`:**")
                for a in arts:
                    output_lines.append(f"- `(:Chapter {c_num})` $\\rightarrow$ `[:CONTAINS_ARTICLE]` $\\rightarrow$ `(:Article)`: **มาตรา {a['num']}: {a['title']}** ({a['summary'][:90]}...)")
                output_lines.append("")
                
            # Misconducts
            miscs = s.run("""
                MATCH (c:Chapter {chapter_number: $c_num})-[:DEFINES_MISCONDUCT]->(m:Misconduct)
                OPTIONAL MATCH (m)-[:SUBJECT_TO]->(p:DisciplinaryPenalty)
                RETURN m.name_th AS name, m.severity AS sev, p.level AS p_level, p.name AS p_name
            """, {"c_num": c_num}).data()
            if miscs:
                output_lines.append(f"**2. ความผิดทางวินัยและบทลงโทษ (`:Misconduct` & `:DisciplinaryPenalty`):**")
                for m in miscs:
                    p_txt = f"**ขั้นที่ {m['p_level']}** ({m['p_name']})" if m['p_level'] else "ยังไม่มีการผูกบทลงโทษ"
                    output_lines.append(f"- `(:Chapter {c_num})` $\\rightarrow$ `[:DEFINES_MISCONDUCT]` $\\rightarrow$ `(:Misconduct {{name: '{m['name']}', severity: '{m['sev']}'}})` $\\rightarrow$ `[:SUBJECT_TO]` $\\rightarrow$ `(:DisciplinaryPenalty)` {p_txt}")
                output_lines.append("")
                
            # Procedures
            procs = s.run("""
                MATCH (c:Chapter {chapter_number: $c_num})-[:HAS_STEP]->(pr:ProcedureStep)
                RETURN pr.step_number AS step, pr.action AS action, pr.timeline_days AS days, pr.responsible AS resp
                ORDER BY pr.step_number
            """, {"c_num": c_num}).data()
            if procs:
                output_lines.append(f"**3. ลำดับขั้นตอนและกระบวนการ (`:ProcedureStep`) เชื่อมโยงด้วย `[:HAS_STEP]`:**")
                for pr in procs:
                    days_txt = f"ภายใน **{pr['days']} วัน**" if pr['days'] else "ไม่มีกำหนดกรอบวัน"
                    output_lines.append(f"- `(:Chapter {c_num})` $\\rightarrow$ `[:HAS_STEP]` $\\rightarrow$ `(:ProcedureStep {{step: {pr['step']}}})`: **{pr['action']}** (กรอบเวลา: {days_txt}, ผู้รับผิดชอบ: `{pr['resp']}`)")
                output_lines.append("")
                
            # Exceptions
            excs = s.run("""
                MATCH (c:Chapter {chapter_number: $c_num})-[:HAS_EXCEPTION]->(ex:LegalException)
                RETURN ex.name AS name, ex.description AS desc
            """, {"c_num": c_num}).data()
            if excs:
                output_lines.append(f"**4. ข้อยกเว้นทางกฎหมาย (`:LegalException`) เชื่อมโยงด้วย `[:HAS_EXCEPTION]`:**")
                for e in excs:
                    output_lines.append(f"- `(:Chapter {c_num})` $\\rightarrow$ `[:HAS_EXCEPTION]` $\\rightarrow$ `(:LegalException)`: **{e['name']}** ({e['desc'][:100]}...)")
                output_lines.append("")
            
            output_lines.append("---\n")
            
    with open("data/knowledge_graph/chapter_connections_dump.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"Exported {len(output_lines)} lines to data/knowledge_graph/chapter_connections_dump.txt")

if __name__ == "__main__":
    export_markdown()
