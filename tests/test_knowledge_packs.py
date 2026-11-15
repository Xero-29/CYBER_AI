import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class KnowledgePackTests(unittest.TestCase):
 def test_every_catalog_area_has_an_offline_pack(self):
  c=json.loads((ROOT/'data/knowledge_sources/knowledge_catalog.json').read_text(encoding='utf-8'))
  m=json.loads((ROOT/'knowledge/packs/manifest.json').read_text(encoding='utf-8'))
  self.assertEqual({a['id'] for a in c['areas']},{a['id'] for a in m['areas']})
  self.assertEqual(len(m['areas']),m['area_count'])
  for a in m['areas']:
   p=ROOT/a['path']; self.assertTrue(p.is_file(),a['id']); s=p.read_text(encoding='utf-8')
   for h in ('## Propósito y límites','## Competencias','## Metodología reproducible','## Laboratorio seguro','## Evaluación','## Instrucciones para agentes IA'): self.assertIn(h,s,a['id'])
 def test_external_sources_are_not_marked_downloaded(self):
  c=json.loads((ROOT/'data/knowledge_sources/knowledge_catalog.json').read_text(encoding='utf-8'))
  for r in c['resources']: self.assertFalse(r['download']); self.assertFalse(r['verified_for_download']); self.assertEqual(r['license_status'],'pending')
if __name__=='__main__': unittest.main()
