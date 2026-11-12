import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import skillbook
class SkillbookTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.p=patch.object(skillbook,"DB_PATH",Path(self.tmp.name)/"s.db"); self.p.start(); skillbook.initialize()
 def tearDown(self): self.p.stop(); self.tmp.cleanup()
 def add(self,**kw):
  d=dict(name="Auditoria cabeceras HTTP",task_pattern="auditoria web revision cabeceras HTTP",description="Revisión defensiva de cabeceras",prerequisites=["objetivo autorizado"],methodology=["solicitar raíz con timeout","comparar cabeceras con OWASP","documentar evidencia"],validation=["repetir solicitud","guardar evidencia anonimizada"],tools=["requests"],tags=["web","http","headers"],evidence=["laboratorio A","laboratorio B"],source_urls=["https://owasp.org/"],success_runs=2,failure_runs=0,verified_by="VERITAS",verifier_verdict="RESPALDADA"); d.update(kw); return skillbook.register_verified_skill(**d)
 def test_retrieval(self):
  x=self.add(); ctx,m=skillbook.build_skill_context("auditoria web revisar cabeceras HTTP"); self.assertIn(x["skill_id"],ctx); self.assertEqual(m[0]["skill_id"],x["skill_id"])
 def test_requires_veritas(self):
  with self.assertRaises(ValueError): self.add(verified_by="NEXO")
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

 def test_no_match(self):
  self.add(); self.assertEqual(skillbook.build_skill_context("analisis forense RAM"),("",[]))
if __name__=="__main__": unittest.main()
