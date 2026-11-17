from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from knowledge_research_audit import audit_research_library


class ResearchAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "knowledge/packs").mkdir(parents=True)
        (self.root / "knowledge/curricula").mkdir(parents=True)
        (self.root / "knowledge/research").mkdir(parents=True)
        (self.root / "knowledge/deep_modules/demo").mkdir(parents=True)
        manifest = {"areas": [{"id": "demo"}]}
        curriculum = {"areas": [{"id": "demo"}]}
        registry = {
            "sources": [{
                "id": "SRC-1",
                "title": "Official source",
                "publisher": "NIST",
                "url": "https://example.org/source",
                "verification_status": "official_metadata_verified",
                "review_note": "Metadata reviewed",
                "domains": ["demo"],
            }]
        }
        (self.root / "knowledge/packs/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.root / "knowledge/curricula/domain_curriculum.json").write_text(
            json.dumps(curriculum), encoding="utf-8"
        )
        (self.root / "knowledge/research/source_registry.json").write_text(
            json.dumps(registry), encoding="utf-8"
        )
        (self.root / "knowledge/research/RESEARCH_PROTOCOL.md").write_text(
            "Reproducción y amenazas a la validez", encoding="utf-8"
        )
        agenda = """# Agenda de investigación: Demo
## Pregunta central
Hipótesis falsable. Método reproducible. Métricas. Entregable. Madurez research_agenda_defined.
M5 requiere revisión y reproducción independiente.
"""
        (self.root / "knowledge/deep_modules/demo/RESEARCH_AGENDA.md").write_text(
            agenda, encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_dossier(self, source_id: str = "SRC-1") -> None:
        dossier = f"""# Revisión de literatura inicial — Demo

**Corte:** 2026-11-17
**Madurez:** M1 documental; no M3/M4.

## Pregunta
¿Cómo se evalúa el problema?

## Síntesis
La fuente primaria define el marco y sus límites.

## Brechas
Lectura integral y experimento pendientes.

## Identificadores del registro de fuentes
- `{source_id}`

Referencia: https://example.org/source
"""
        (self.root / "knowledge/deep_modules/demo/LITERATURE_REVIEW.md").write_text(
            dossier, encoding="utf-8"
        )

    def test_accepts_complete_agenda_structure(self) -> None:
        report = audit_research_library(self.root)
        self.assertTrue(report["ok"])
        self.assertEqual(report["agenda_count"], 1)
        self.assertEqual(report["structurally_complete_agendas"], 1)
        self.assertEqual(report["source_count"], 1)
        self.assertFalse(report["coverage_complete"])

    def test_detects_missing_agenda(self) -> None:
        (self.root / "knowledge/deep_modules/demo/RESEARCH_AGENDA.md").unlink()
        report = audit_research_library(self.root)
        self.assertFalse(report["ok"])
        self.assertEqual(report["agenda_count"], 0)

    def test_does_not_claim_scientific_validation(self) -> None:
        report = audit_research_library(self.root)
        self.assertTrue(any("No demuestra" in item for item in report["limitations"]))
        self.assertNotIn("maturity", report)

    def test_rejects_missing_source_metadata(self) -> None:
        registry_path = self.root / "knowledge/research/source_registry.json"
        registry_path.write_text(json.dumps({"sources": [{"id": "BAD"}]}), encoding="utf-8")
        report = audit_research_library(self.root)
        self.assertFalse(report["ok"])
        self.assertTrue(any("fuente sin title" in error for error in report["errors"]))

    def test_counts_traceable_literature_review(self) -> None:
        self.write_dossier()
        report = audit_research_library(self.root)
        self.assertTrue(report["ok"])
        self.assertEqual(report["literature_review_count"], 1)
        self.assertEqual(report["traceable_literature_reviews"], 1)
        self.assertEqual(report["unique_source_ids_referenced_by_dossiers"], 1)

    def test_rejects_unknown_source_reference(self) -> None:
        self.write_dossier("UNKNOWN-SOURCE")
        report = audit_research_library(self.root)
        self.assertTrue(report["ok"])
        self.assertEqual(report["traceable_literature_reviews"], 0)
        self.assertTrue(any(
            "ID de fuente no registrado" in error
            for error in report["areas"][0]["literature_review_errors"]
        ))


    def test_accepts_dotted_source_identifier(self) -> None:
        registry_path = self.root / "knowledge/research/source_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["sources"][0]["id"] = "OWASP-ASVS-5.0.0"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        self.write_dossier("OWASP-ASVS-5.0.0")
        report = audit_research_library(self.root)
        self.assertEqual(report["traceable_literature_reviews"], 1)

    def test_requires_https_source_urls(self) -> None:
        registry_path = self.root / "knowledge/research/source_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["sources"][0]["url"] = "http://example.org/source"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        report = audit_research_library(self.root)
        self.assertFalse(report["ok"])
        self.assertTrue(any("HTTPS" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
