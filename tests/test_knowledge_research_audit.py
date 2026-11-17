from __future__ import annotations

import json
from pathlib import Path

from knowledge_research_audit import audit_research_library


def _fixture(tmp_path: Path) -> Path:
    (tmp_path / "knowledge/packs").mkdir(parents=True)
    (tmp_path / "knowledge/curricula").mkdir(parents=True)
    (tmp_path / "knowledge/research").mkdir(parents=True)
    (tmp_path / "knowledge/deep_modules/demo").mkdir(parents=True)
    manifest = {"areas": [{"id": "demo"}]}
    curriculum = {"areas": [{"id": "demo"}]}
    registry = {"sources": [{"id": "s1", "title": "Official source", "publisher": "NIST", "url": "https://example.org", "verification_status": "official_metadata_verified", "review_note": "Metadata reviewed"}]}
    (tmp_path / "knowledge/packs/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / "knowledge/curricula/domain_curriculum.json").write_text(json.dumps(curriculum), encoding="utf-8")
    (tmp_path / "knowledge/research/source_registry.json").write_text(json.dumps(registry), encoding="utf-8")
    (tmp_path / "knowledge/research/RESEARCH_PROTOCOL.md").write_text("Reproducción y amenazas a la validez", encoding="utf-8")
    agenda = """# Agenda de investigación: Demo
## Pregunta central
Hipótesis falsable. Método reproducible. Métricas. Entregable. Madurez research_agenda_defined.
M5 requiere revisión y reproducción independiente.
"""
    (tmp_path / "knowledge/deep_modules/demo/RESEARCH_AGENDA.md").write_text(agenda, encoding="utf-8")
    return tmp_path


def test_audit_accepts_complete_research_agenda_structure(tmp_path: Path) -> None:
    report = audit_research_library(_fixture(tmp_path))
    assert report["ok"] is True
    assert report["agenda_count"] == 1
    assert report["structurally_complete_agendas"] == 1
    assert report["source_count"] == 1


def test_audit_detects_missing_agenda(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    (root / "knowledge/deep_modules/demo/RESEARCH_AGENDA.md").unlink()
    report = audit_research_library(root)
    assert report["ok"] is False
    assert report["agenda_count"] == 0


def test_audit_does_not_claim_scientific_validation(tmp_path: Path) -> None:
    report = audit_research_library(_fixture(tmp_path))
    assert any("No demuestra" in item for item in report["limitations"])
    assert "M4" not in str(report.get("maturity", ""))


def test_audit_rejects_missing_source_metadata(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    (root / "knowledge/research/source_registry.json").write_text(json.dumps({"sources": [{"id": "bad"}]}), encoding="utf-8")
    report = audit_research_library(root)
    assert report["ok"] is False
    assert any("fuente sin title" in error for error in report["errors"])
