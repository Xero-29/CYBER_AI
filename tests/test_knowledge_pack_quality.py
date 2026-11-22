import json
import tempfile
import unittest
from pathlib import Path

from knowledge_pack_quality import audit_packs


class KnowledgePackQualityTests(unittest.TestCase):
    def test_current_48_packs_are_not_misreported_as_expert_ready(self):
        report = audit_packs()
        self.assertEqual(report["status"], "audited")
        self.assertEqual(report["area_count"], 48)
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["foundation_draft_count"], 48)
        self.assertTrue(all(not item["expert_ready"] for item in report["areas"]))
        self.assertTrue(all(item["verified_external_sources"] == 0 for item in report["areas"]))

    def _write_expert_fixture(self, root):
        pack = root / "knowledge" / "packs" / "sample.md"
        pack.parent.mkdir(parents=True)
        headings = (
            "Propósito y límites",
            "Fundamentos",
            "Arquitectura",
            "Modelo de amenazas",
            "Competencias",
            "Mecanismos técnicos",
            "Controles",
            "Metodología",
            "Ejemplos desarrollados",
            "Laboratorio",
            "Reproducibilidad",
            "Evaluación",
            "Fuentes verificables",
            "Instrucciones para agentes IA",
        )
        pack.write_text(
            "\n".join(f"## {heading}\nContenido técnico reproducible." for heading in headings),
            encoding="utf-8",
        )
        sources_path = root / "knowledge" / "packs" / "sources.json"
        sources_path.write_text(json.dumps({
            "sources": [{
                "id": f"source-{index}",
                "title": f"Fuente {index}",
                "publisher": "Organismo oficial",
                "url": f"https://example.org/source-{index}",
                "version": "2026-01",
                "license": "CC BY 4.0",
                "license_status": "approved",
                "verified_at": "2026-11-22T00:00:00Z",
                "verification_evidence": f"revisión independiente {index}",
            } for index in range(5)]
        }), encoding="utf-8")
        lab_path = root / "knowledge" / "packs" / "lab.json"
        lab_path.write_text(json.dumps({
            "runs": [{
                "status": "passed",
                "artifact_sha256": "a" * 64,
                "executed_at": "2026-11-22T00:00:00Z",
                "environment": "Linux isolated lab",
                "command": "pytest -q",
                "scope": "authorized local lab",
            }]
        }), encoding="utf-8")
        review_path = root / "knowledge" / "packs" / "review.json"
        review_path.write_text(json.dumps({
            "decision": "approved",
            "independent_review": True,
            "reviewer_id": "independent-reviewer",
            "reviewed_at": "2026-11-22T00:00:00Z",
            "reviewed_commit": "b" * 40,
            "evidence": ["technical review", "lab reproduction"],
        }), encoding="utf-8")
        manifest_path = root / "knowledge" / "packs" / "manifest.json"
        manifest_path.write_text(json.dumps({
            "area_count": 1,
            "areas": [{
                "id": "sample",
                "name": "Sample",
                "path": "knowledge/packs/sample.md",
                "source_registry_path": "knowledge/packs/sources.json",
                "lab_evidence_path": "knowledge/packs/lab.json",
                "quality_review_path": "knowledge/packs/review.json",
            }],
        }), encoding="utf-8")
        return manifest_path

    def test_expert_ready_requires_complete_sections_sources_lab_and_independent_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._write_expert_fixture(root)
            report = audit_packs(manifest, root=root)
        self.assertEqual(report["expert_ready_count"], 1)
        self.assertTrue(report["areas"][0]["expert_ready"])
        self.assertEqual(report["areas"][0]["missing_sections"], [])

    def test_pending_source_license_prevents_expert_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._write_expert_fixture(root)
            sources = root / "knowledge" / "packs" / "sources.json"
            data = json.loads(sources.read_text(encoding="utf-8"))
            data["sources"][0]["license_status"] = "pending"
            sources.write_text(json.dumps(data), encoding="utf-8")
            report = audit_packs(manifest, root=root)
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["areas"][0]["verified_external_sources"], 4)

    def test_path_traversal_in_pack_manifest_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self._write_expert_fixture(root)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["areas"][0]["path"] = "../outside.md"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            report = audit_packs(manifest, root=root)
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["areas"][0]["quality_status"], "foundation_draft")
        self.assertIsNotNone(report["areas"][0]["path_error"])


if __name__ == "__main__":
    unittest.main()
