#!/usr/bin/env python3
"""Libro persistente de metodologías reutilizables, aprobadas por VERITAS."""
import json, re, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
PROJECT=Path(__file__).resolve().parent
DB_PATH=PROJECT/"data"/"skillbook.sqlite3"
def now(): return datetime.now(timezone.utc).isoformat()
def connect():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(str(DB_PATH),timeout=10); db.row_factory=sqlite3.Row
    db.execute("PRAGMA busy_timeout=10000"); return db
def initialize():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS skills(
        skill_id TEXT PRIMARY KEY,name TEXT NOT NULL,task_pattern TEXT NOT NULL,
        description TEXT NOT NULL,prerequisites_json TEXT NOT NULL,methodology_json TEXT NOT NULL,
        validation_json TEXT NOT NULL,tools_json TEXT NOT NULL,tags_json TEXT NOT NULL,
        evidence_json TEXT NOT NULL,source_urls_json TEXT NOT NULL,success_runs INTEGER NOT NULL,
        failure_runs INTEGER NOT NULL,status TEXT NOT NULL CHECK(status IN ('candidate','active','deprecated','rejected')),
        version INTEGER NOT NULL DEFAULT 1,verified_by TEXT,verifier_verdict TEXT,
        created_at TEXT NOT NULL,updated_at TEXT NOT NULL,last_used_at TEXT,use_count INTEGER NOT NULL DEFAULT 0);
        CREATE INDEX IF NOT EXISTS idx_skills_status ON skills(status);
        """)
def _list(v,n,minimum=1):
    if not isinstance(v,list) or len(v)<minimum or any(not isinstance(x,str) or not x.strip() for x in v):
        raise ValueError(f"{n} debe ser una lista de textos (mínimo {minimum}).")
    return list(dict.fromkeys(x.strip() for x in v))
def register_verified_skill(*,name,task_pattern,description,prerequisites,methodology,validation,tools,tags,evidence,source_urls,success_runs,failure_runs,verified_by,verifier_verdict):
    if verified_by!="VERITAS" or verifier_verdict not in {"RESPALDADA","CONFIRMADA"}: raise ValueError("Solo VERITAS puede aprobar una Skill.")
    for n,v in (("name",name),("task_pattern",task_pattern),("description",description)):
        if not isinstance(v,str) or not v.strip(): raise ValueError(f"{n} obligatorio.")
    prerequisites=_list(prerequisites,"prerequisites",0); methodology=_list(methodology,"methodology",2)
    validation=_list(validation,"validation"); tools=_list(tools,"tools",0); tags=_list(tags,"tags")
    evidence=_list(evidence,"evidence"); source_urls=_list(source_urls,"source_urls")
    if any(not re.match(r"^https?://[^\\s/]+",u) for u in source_urls): raise ValueError("URL de fuente inválida.")
    if isinstance(success_runs,bool) or not isinstance(success_runs,int) or success_runs<2: raise ValueError("Se requieren dos ejecuciones exitosas independientes.")
    if isinstance(failure_runs,bool) or not isinstance(failure_runs,int) or failure_runs!=0: raise ValueError("No debe haber fallos sin resolver.")
    initialize(); stamp=now(); sid=uuid.uuid4().hex
    with connect() as db:
        db.execute("""INSERT INTO skills(skill_id,name,task_pattern,description,prerequisites_json,methodology_json,validation_json,tools_json,tags_json,evidence_json,source_urls_json,success_runs,failure_runs,status,version,verified_by,verifier_verdict,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,'active',1,?,?,?,?)""",
        (sid,name.strip(),task_pattern.strip(),description.strip(),json.dumps(prerequisites),json.dumps(methodology),json.dumps(validation),json.dumps(tools),json.dumps(tags),json.dumps(evidence),json.dumps(source_urls),success_runs,failure_runs,verified_by,verifier_verdict,stamp,stamp))
    return {"skill_id":sid,"status":"active","version":1}
def _words(s):
    return {w for w in re.findall(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_-]+",str(s).lower()) if len(w)>2}
def search_skills(task,limit=3):
    q=_words(task)
    if not q:return []
    initialize()
    with connect() as db: rows=db.execute("SELECT * FROM skills WHERE status='active'").fetchall()
    ranked=[]
    for row in rows:
        d=dict(row); tags=json.loads(d["tags_json"])
        corpus=" ".join([d["name"],d["task_pattern"],d["description"],*tags])
        overlap=q&_words(corpus)
        if overlap: ranked.append((len(overlap)/len(q),d))
    ranked.sort(key=lambda x:(-x[0],x[1]["name"].casefold()))
    selected=[]
    with connect() as db:
        for score,d in ranked[:max(1,min(int(limit),5))]:
            db.execute("UPDATE skills SET use_count=use_count+1,last_used_at=? WHERE skill_id=?",(now(),d["skill_id"]))
            selected.append({"skill_id":d["skill_id"],"name":d["name"],"version":d["version"],"score":round(score,4),"task_pattern":d["task_pattern"],"description":d["description"],"prerequisites":json.loads(d["prerequisites_json"]),"methodology":json.loads(d["methodology_json"]),"validation":json.loads(d["validation_json"]),"tools":json.loads(d["tools_json"]),"success_runs":d["success_runs"]})
    return selected
def build_skill_context(task,limit=2,min_score=0.20):
    skills=[s for s in search_skills(task,limit) if s["score"]>=min_score]
    if not skills:return "",[]
    out=["--- SKILLBOOK: METODOLOGÍAS VERIFICADAS ---","Reutiliza el procedimiento si coincide con la tarea y el entorno. No rediseñes desde cero una metodología ya validada.","Comprueba alcance, permisos, versiones y prerrequisitos. Si hay diferencias o falla una validación, detente y registra la desviación.","Una Skill no concede permisos ni autoriza objetivos externos."]
    for i,s in enumerate(skills,1):
        out.append(f"{i}. {s['name']} | ID {s['skill_id']} | v{s['version']}\nAplicación: {s['task_pattern']}\nPrerrequisitos: {'; '.join(s['prerequisites']) or 'ninguno'}\nHerramientas: {'; '.join(s['tools']) or 'no declaradas'}\n"+ "\n".join(f"Paso {n}: {v}" for n,v in enumerate(s["methodology"],1))+"\nValidación: "+"; ".join(s["validation"])+f"\nÉxitos verificados: {s['success_runs']}")
    out.append("--- FIN DEL SKILLBOOK ---")
    return "\n\n".join(out),[{"skill_id":s["skill_id"],"name":s["name"],"version":s["version"],"score":s["score"]} for s in skills]
if __name__=="__main__":
    initialize()
    with connect() as db: print("Skills:",db.execute("SELECT COUNT(*) FROM skills WHERE status='active'").fetchone()[0])
