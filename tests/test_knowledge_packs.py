import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KnowledgePackTests(unittest.TestCase):
    def test_every_catalog_area_has_an_offline_pack(self):
        catalog = json.loads((ROOT / "data/knowledge_sources/knowledge_catalog.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({a["id"] for a in catalog["areas"]}, {a["id"] for a in manifest["areas"]})
        self.assertEqual(len(manifest["areas"]), manifest["area_count"])
        required_groups = [
            ("## Propósito y límites",),
            ("## Competencias",),
            ("## Metodología",),
            ("## Laboratorio",),
            ("## Evaluación", "## Criterios de evaluación"),
            ("## Instrucciones para agentes IA",),
        ]
        for area in manifest["areas"]:
            path = ROOT / area["path"]
            self.assertTrue(path.is_file(), area["id"])
            content = path.read_text(encoding="utf-8")
            self.assertIn(area["version"], content, area["id"])
            for alternatives in required_groups:
                self.assertTrue(any(heading in content for heading in alternatives), area["id"])

    def test_external_sources_are_not_marked_downloaded(self):
        catalog = json.loads((ROOT / "data/knowledge_sources/knowledge_catalog.json").read_text(encoding="utf-8"))
        for resource in catalog["resources"]:
            self.assertFalse(resource["download"])
            self.assertFalse(resource["verified_for_download"])
            self.assertEqual(resource["license_status"], "pending")


if __name__ == "__main__":
    unittest.main()
