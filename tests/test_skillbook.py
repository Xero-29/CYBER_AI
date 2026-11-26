import hashlib, hmac, json, os, sqlite3, stat, tempfile, unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
import skillbook
class SkillbookTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.p=patch.object(skillbook,"DB_PATH",Path(self.tmp.name)/"s.db"); self.p.start(); skillbook.initialize()
 def tearDown(self): self.p.stop(); self.tmp.cleanup()
 @unittest.skipUnless(os.name == "posix", "POSIX file permissions required")
 def test_skillbook_database_is_private(self):
  self.assertEqual(stat.S_IMODE(skillbook.DB_PATH.stat().st_mode),0o600)
  self.assertEqual(stat.S_IMODE(skillbook.DB_PATH.parent.stat().st_mode),0o700)
 def add(self,**kw):
  d=dict(name="Auditoria cabeceras HTTP",task_pattern="auditoria web revision cabeceras HTTP",description="Revisión defensiva de cabeceras",prerequisites=["objetivo autorizado"],methodology=["solicitar raíz con timeout","comparar cabeceras con OWASP","documentar evidencia"],validation=["repetir solicitud","guardar evidencia anonimizada"],tools=["requests"],tags=["web","http","headers"],evidence=["laboratorio A","laboratorio B"],source_urls=["https://owasp.org/"],success_runs=2,failure_runs=0,verified_by="VERITAS",verifier_verdict="RESPALDADA"); d.update(kw); return skillbook._insert_verified_skill(**d)
 def test_retrieval(self):
  x=self.add(); ctx,m=skillbook.build_skill_context("auditoria web revisar cabeceras HTTP"); self.assertIn(x["skill_id"],ctx); self.assertEqual(m[0]["skill_id"],x["skill_id"])
 def test_skills_due_for_review_uses_last_update_not_last_use(self):
  stale=self.add(name="Skill antigua")
  fresh=self.add(name="Skill reciente",task_pattern="tarea reciente")
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET updated_at=? WHERE skill_id=?",("2000-01-01T00:00:00+00:00",stale["skill_id"]))
  due=skillbook.list_skills_due_for_review(max_age_days=180)
  self.assertEqual([item["skill_id"] for item in due],[stale["skill_id"]])
  self.assertEqual(due[0]["reason"],"review_age_exceeded")
  self.assertEqual(due[0]["version"],1)
  with self.assertRaises(ValueError):
   skillbook.list_skills_due_for_review(max_age_days=0)

 def test_invalid_skill_review_timestamp_is_flagged(self):
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET updated_at=? WHERE skill_id=?",("not-a-date",skill["skill_id"]))
  due=skillbook.list_skills_due_for_review()
  self.assertEqual(len(due),1)
  self.assertEqual(due[0]["reason"],"invalid_review_timestamp")
  self.assertIsNone(due[0]["review_due_at"])

 def test_skill_history_verifies_contiguous_versions_and_current_snapshot(self):
  skill=self.add()
  result=skillbook.verify_skill_history(skill["skill_id"])
  self.assertTrue(result["valid"],result)
  self.assertEqual(result["versions_checked"],1)
  self.assertEqual(result["current_version"],1)

 def test_skill_history_detects_current_snapshot_mismatch(self):
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET name=? WHERE skill_id=?",("tampered name",skill["skill_id"]))
  result=skillbook.verify_skill_history(skill["skill_id"])
  self.assertFalse(result["valid"])
  self.assertEqual(result["reason"],"current_snapshot_mismatch")
  self.assertIn("name",result["fields"])

 def test_skill_history_detects_missing_version(self):
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET version=3 WHERE skill_id=?",(skill["skill_id"],))
  result=skillbook.verify_skill_history(skill["skill_id"])
  self.assertFalse(result["valid"])
  self.assertEqual(result["reason"],"version_sequence")

 def test_skill_history_migrates_legacy_version_table(self):
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("DROP TRIGGER skill_versions_no_update")
   db.execute("DROP TRIGGER skill_versions_no_delete")
   db.execute("DROP INDEX idx_skill_versions_skill")
   db.execute("ALTER TABLE skill_versions RENAME TO skill_versions_legacy")
   db.execute("""CREATE TABLE skill_versions(
    skill_id TEXT NOT NULL,version INTEGER NOT NULL,change_type TEXT NOT NULL,
    actor TEXT NOT NULL,snapshot_json TEXT NOT NULL,created_at TEXT NOT NULL,
    PRIMARY KEY(skill_id,version))""")
   db.execute("""INSERT INTO skill_versions
    SELECT skill_id,version,change_type,actor,snapshot_json,created_at
    FROM skill_versions_legacy""")
   db.execute("DROP TABLE skill_versions_legacy")
  result=skillbook.verify_skill_history(skill["skill_id"])
  self.assertTrue(result["valid"],result)
  with skillbook.connect() as db:
   row=db.execute("SELECT previous_hash,entry_hash FROM skill_versions WHERE skill_id=?",(skill["skill_id"],)).fetchone()
  self.assertEqual(row["previous_hash"],skillbook.VERSION_HASH_GENESIS)
  self.assertEqual(len(row["entry_hash"]),64)

 def test_skill_history_detects_tampered_historical_snapshot(self):
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET version=2,description=? WHERE skill_id=?",("Nueva descripción",skill["skill_id"]))
   skillbook._save_version(db,skill["skill_id"],2,"updated","VERITAS")
  self.assertTrue(skillbook.verify_skill_history(skill["skill_id"])["valid"])
  with skillbook.connect() as db:
   db.execute("DROP TRIGGER skill_versions_no_update")
   db.execute("UPDATE skill_versions SET snapshot_json=? WHERE skill_id=? AND version=1",("{}",skill["skill_id"]))
  result=skillbook.verify_skill_history(skill["skill_id"])
  self.assertFalse(result["valid"])
  self.assertEqual(result["reason"],"history_hash_chain")
  self.assertEqual(result["failed_version"],1)

 def test_public_registration_cannot_self_assert_veritas(self):
  with self.assertRaisesRegex(ValueError,"(?i)registro directo deshabilitado"):
   skillbook.register_verified_skill(verified_by="VERITAS",verifier_verdict="CONFIRMADA")
 def test_requires_two_successes_and_zero_failures(self):
  with self.assertRaises(ValueError): self.add(success_runs=1)
  with self.assertRaises(ValueError): self.add(failure_runs=1)
 def test_accepts_valid_host_containing_letter_s(self):
  result=self.add(source_urls=["https://security.example.com/"])
  self.assertEqual(result["status"],"active")

 def test_rejects_invalid_source_urls(self):
  for url in ("https:///missing-host", "https://user:pass@example.com/", "https://bad host.example/"):
   with self.subTest(url=url), self.assertRaises(ValueError):
    self.add(source_urls=[url])

 def test_ledger_promotion_requires_signed_independent_evidence(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  events=[
   {"event_id":"run-1","task_fingerprint":"f"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-01-01T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"a"*64},
   {"event_id":"run-2","task_fingerprint":"f"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-01-02T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"b"*64},
  ]
  class FakeLedger:
   def verify(self): return {"valid":True}
   def history(self,**kwargs): return events
  args=dict(name="Skill firmada",task_pattern="misma tarea de prueba",description="Procedimiento respaldado",prerequisites=["entorno de prueba"],methodology=["preparar entorno","ejecutar comprobación"],validation=["verificar resultado"],tools=["ruff"],tags=["test","quality"],source_urls=["https://example.org/"],namespace="nexo",event_ids=["run-1","run-2"])
  with patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   payload=skillbook.skill_approval_payload(**args)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   result=skillbook.register_skill_from_ledger(**args,approval_signature=signature)
  self.assertEqual(result["status"],"active")
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   with self.assertRaisesRegex(ValueError,"Firma VERITAS inválida"):
    skillbook.register_skill_from_ledger(**args,approval_signature="0"*64)
  events.append({"event_id":"run-3","task_fingerprint":"f"*64,"status":"failed","created_at":"2026-01-03T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":False,"independent":True,"evidence":["review"]}],"evidence_sha256":"c"*64})
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   with self.assertRaisesRegex(ValueError,"Hay ejecuciones fallidas"):
    skillbook.register_skill_from_ledger(**args,approval_signature=signature)

 def test_concurrent_signed_promotions_create_only_one_skill(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  events=[
   {"event_id":"concurrent-run-1","task_fingerprint":"9"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-05-01T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"a"*64},
   {"event_id":"concurrent-run-2","task_fingerprint":"9"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-05-02T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"b"*64},
  ]
  class FakeLedger:
   def verify(self): return {"valid":True}
   def history(self,**kwargs): return events
  args=dict(name="Skill concurrente",task_pattern="promocion concurrente unica",description="Debe evitar duplicados",prerequisites=[],methodology=["preparar fixture","verificar firma"],validation=["contar registros"],tools=[],tags=["concurrency"],source_urls=[],namespace="concurrency",event_ids=["concurrent-run-1","concurrent-run-2"])
  with patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   payload=skillbook.skill_approval_payload(**args)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   with ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(
     lambda _: skillbook.register_skill_from_ledger(**args,approval_signature=signature),
     range(2),
    ))
  self.assertEqual(results[0]["skill_id"],results[1]["skill_id"])
  with skillbook.connect() as db:
   count=db.execute("SELECT COUNT(*) FROM skills WHERE task_pattern=?",(args["task_pattern"],)).fetchone()[0]
  self.assertEqual(count,1)
  self.assertEqual(len(skillbook.list_skill_versions(results[0]["skill_id"])),1)

 def test_started_lifecycle_events_do_not_invalidate_successful_skill_evidence(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  events=[
   {"event_id":"start-1","task_fingerprint":"e"*64,"status":"started","created_at":"2026-03-01T00:00:00Z"},
   {"event_id":"run-1","task_fingerprint":"e"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-03-01T00:01:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"a"*64},
   {"event_id":"start-2","task_fingerprint":"e"*64,"status":"started","created_at":"2026-03-02T00:00:00Z"},
   {"event_id":"run-2","task_fingerprint":"e"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-03-02T00:01:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"b"*64},
  ]
  class FakeLedger:
   def verify(self): return {"valid":True}
   def history(self,**kwargs): return events
  args=dict(name="Skill lifecycle",task_pattern="tarea lifecycle verificada",description="Procedimiento validado",prerequisites=["fixture"],methodology=["preparar fixture","ejecutar prueba"],validation=["verificar resultado"],tools=["ruff"],tags=["test","lifecycle"],source_urls=["https://example.org/"],namespace="nexo",event_ids=["run-1","run-2"])
  with patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   payload=skillbook.skill_approval_payload(**args)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   result=skillbook.register_skill_from_ledger(**args,approval_signature=signature)
  self.assertEqual(result["status"],"active")

 def test_empty_source_urls_are_allowed_for_ledger_only_evidence(self):
  self.assertEqual(skillbook._validate_source_urls([]), [])

 def test_candidate_is_not_searchable_until_signed_promotion(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  events=[
   {"event_id":"candidate-run-1","task_fingerprint":"d"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-02-01T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"1"*64},
   {"event_id":"candidate-run-2","task_fingerprint":"d"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-02-02T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"2"*64},
  ]
  class FakeLedger:
   def verify(self): return {"valid":True}
   def history(self,**kwargs): return events
  args=dict(name="Skill candidata",task_pattern="tarea repetible y segura",description="Metodología validada en pruebas",prerequisites=["entorno aislado"],methodology=["preparar fixture","ejecutar verificación"],validation=["comparar salida esperada"],tools=["ruff"],tags=["testing","quality"],source_urls=["https://example.org/"],namespace="forja",event_ids=["candidate-run-1","candidate-run-2"])
  with patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   candidate=skillbook.propose_skill_from_ledger(**args)
   repeated=skillbook.propose_skill_from_ledger(**args)
  self.assertEqual(candidate["status"],"candidate")
  self.assertTrue(repeated["reused"])
  self.assertEqual(skillbook.search_skills("tarea repetible"),[])
  versions=skillbook.list_skill_versions(candidate["skill_id"])
  self.assertEqual([v["change_type"] for v in versions],["proposed"])
  with patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   payload=skillbook.skill_approval_payload(**args)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   promoted=skillbook.register_skill_from_ledger(**args,approval_signature=signature)
  self.assertEqual(promoted["skill_id"],candidate["skill_id"])
  self.assertEqual(promoted["version"],2)
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   repeated=skillbook.register_skill_from_ledger(**args,approval_signature=signature)
  self.assertEqual(repeated["skill_id"],candidate["skill_id"])
  self.assertEqual(repeated["version"],2)
  self.assertTrue(repeated["reused"])
  self.assertEqual(len(skillbook.search_skills("tarea repetible")),1)
  self.assertEqual(
   [v["change_type"] for v in skillbook.list_skill_versions(candidate["skill_id"])],
   ["proposed","approved"],
  )

 def test_skill_version_history_is_append_only(self):
  skill=self.add()
  skillbook.initialize()
  with skillbook.connect() as db:
   with self.assertRaises(sqlite3.IntegrityError):
    db.execute("DELETE FROM skill_versions WHERE skill_id=?",(skill["skill_id"],))

 def test_self_reported_validator_cannot_promote_skill(self):
  events=[
   {"event_id":"self-run-1","task_fingerprint":"e"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-03-01T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":False,"evidence":["review"]}],"evidence_sha256":"1"*64},
   {"event_id":"self-run-2","task_fingerprint":"e"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-03-02T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":False,"evidence":["review"]}],"evidence_sha256":"2"*64},
  ]
  class FakeLedger:
   def verify(self): return {"valid":True}
   def history(self,**kwargs): return events
  args=dict(name="No independiente",task_pattern="validacion propia",description="No debe aprobarse",prerequisites=[],methodology=["paso uno","paso dos"],validation=["comprobar"],tools=[],tags=["test"],source_urls=["https://example.org/"],namespace="forja",event_ids=["self-run-1","self-run-2"])
  with patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger()):
   with self.assertRaisesRegex(ValueError,"validador independiente"):
    skillbook.propose_skill_from_ledger(**args)

 def test_skill_signature_is_bound_to_evidence_hashes(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  events=[
   {"event_id":"hash-run-1","task_fingerprint":"c"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-04-01T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"1"*64},
   {"event_id":"hash-run-2","task_fingerprint":"c"*64,"status":"completed","tool":"team_orchestrator","metadata":{"objective_supervision":True},"created_at":"2026-04-02T00:00:00Z","validator_results":[{"name":"objective_review:VERITAS","reviewer":"VERITAS","passed":True,"independent":True,"evidence":["review"]}],"evidence_sha256":"2"*64},
  ]
  class FakeLedger:
   def __init__(self,events): self.events=events
   def verify(self): return {"valid":True}
   def history(self,**kwargs): return self.events
  args=dict(name="Firma ligada",task_pattern="evidencia integra",description="Debe detectar cambios",prerequisites=[],methodology=["capturar evidencia","validar firma"],validation=["comparar hashes"],tools=[],tags=["integrity"],source_urls=["https://example.org/"],namespace="forja",event_ids=["hash-run-1","hash-run-2"])
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger(events)):
   payload=skillbook.skill_approval_payload(**args)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  changed=[dict(item) for item in events]
  changed[0]["evidence_sha256"]="9"*64
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}), patch.object(skillbook,"ExecutionLedger",return_value=FakeLedger(changed)):
   with self.assertRaisesRegex(ValueError,"Firma VERITAS inválida"):
    skillbook.register_skill_from_ledger(**args,approval_signature=signature)

 def test_no_match(self):
  self.add(); self.assertEqual(skillbook.build_skill_context("analisis forense RAM"),("",[]))

 def test_signed_rollback_restores_prior_snapshot_and_appends_version(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET name=?,methodology_json=?,version=2,updated_at=? WHERE skill_id=?",("Mutada",'["paso alterado","paso roto"]',skillbook.now(),skill["skill_id"]))
   skillbook._save_version(db,skill["skill_id"],2,"updated","VERITAS")
  payload=skillbook.skill_rollback_payload(skill["skill_id"],1)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}):
   result=skillbook.rollback_skill_version(skill["skill_id"],1,signature)
  self.assertEqual(result["version"],3)
  with skillbook.connect() as db:
   row=db.execute("SELECT * FROM skills WHERE skill_id=?",(skill["skill_id"],)).fetchone()
  self.assertEqual(row["name"],"Auditoria cabeceras HTTP")
  self.assertEqual(json.loads(row["methodology_json"]),["solicitar raíz con timeout","comparar cabeceras con OWASP","documentar evidencia"])
  self.assertEqual(row["verifier_verdict"],"ROLLBACK_APPROVED")
  self.assertEqual([v["change_type"] for v in skillbook.list_skill_versions(skill["skill_id"])],["created","updated","rollback"])

 def test_rollback_rejects_invalid_signature_and_stale_payload(self):
  key="test-veritas-approval-key-with-32-bytes-minimum"
  skill=self.add()
  with skillbook.connect() as db:
   db.execute("UPDATE skills SET name=?,version=2 WHERE skill_id=?",("Mutada",skill["skill_id"]))
   skillbook._save_version(db,skill["skill_id"],2,"updated","VERITAS")
  payload=skillbook.skill_rollback_payload(skill["skill_id"],1)
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}):
   with self.assertRaisesRegex(ValueError,"Firma VERITAS"):
    skillbook.rollback_skill_version(skill["skill_id"],1,"0"*64)
   with skillbook.connect() as db:
    db.execute("UPDATE skills SET name=? WHERE skill_id=?",("Cambio posterior",skill["skill_id"]))
   with self.assertRaisesRegex(ValueError,"Firma VERITAS"):
    skillbook.rollback_skill_version(skill["skill_id"],1,signature)


 def test_signed_revocation_deprecates_skill_and_removes_it_from_retrieval(self):
  key="veritas-revocation-key-with-at-least-32-bytes"
  skill=self.add()
  payload=skillbook.skill_deprecation_payload(skill["skill_id"],"Método obsoleto")
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}):
   result=skillbook.deprecate_skill(skill["skill_id"],"Método obsoleto",signature)
  self.assertEqual(result["status"],"deprecated")
  self.assertEqual(result["version"],2)
  self.assertEqual(skillbook.search_skills("auditoria web cabeceras"),[])
  versions=skillbook.list_skill_versions(skill["skill_id"])
  self.assertEqual([item["change_type"] for item in versions],["created","revoked"])

 def test_revocation_rejects_invalid_signature_and_stale_approval(self):
  key="veritas-revocation-key-with-at-least-32-bytes"
  skill=self.add()
  payload=skillbook.skill_deprecation_payload(skill["skill_id"],"Revocación")
  signature=hmac.new(key.encode(),payload.encode(),hashlib.sha256).hexdigest()
  with patch.dict(os.environ,{"CYBER_AI_VERITAS_APPROVAL_KEY":key}):
   with self.assertRaisesRegex(ValueError,"Firma VERITAS"):
    skillbook.deprecate_skill(skill["skill_id"],"Revocación","0"*64)
   skillbook.deprecate_skill(skill["skill_id"],"Revocación",signature)
   with self.assertRaisesRegex(ValueError,"cambió|Solo se puede revocar"):
    skillbook.deprecate_skill(skill["skill_id"],"Revocación",signature)

if __name__=="__main__": unittest.main()
