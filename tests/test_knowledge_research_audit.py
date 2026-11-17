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
    (tmp_path / "knowledge/packs/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / "knowledge/curricula/domain_curriculum.json").write_text(json.dumps(curriculum), encoding="utf-8")
    (tmp_path / "knowledge/research/source_registry.json").write_text(json.dumps(registry), encoding="utf-8")
    (tmp_path / "knowledge/research/RESEARCH_PROTOCOL.md").write_text(
        "Reproducción y amenazas a la validez", encoding="utf-8"
    )
    agenda = """# Agenda de investigación: Demo
## Pregunta central
Hipótesis falsable. Método reproducible. Métricas. Entregable. Madurez research_agenda_defined.
M5 requiere revisión y reproducción independiente.
"""
    (tmp_path / "knowledge/deep_modules/demo/RESEARCH_AGENDA.md").write_text(agenda, encoding="utf-8")
    return tmp_path


def _write_dossier(root: Path, source_id: str = "SRC-1") -> None:
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
    (root / "knowledge/deep_modules/demo/LITERATURE_REVIEW.md").write_text(dossier, encoding="utf-8")


def test_audit_accepts_complete_research_agenda_structure(tmp_path: Path) -> None:
    report = audit_research_library(_fixture(tmp_path))
    assert report["ok"] is True
    assert report["agenda_count"] == 1
    assert report["structurally_complete_agendas"] == 1
    assert report["source_count"] == 1
    assert report["coverage_complete"] is False


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
    (root / "knowledge/research/source_registry.json").write_text(
        json.dumps({"sources": [{"id": "BAD"}]}), encoding="utf-8"
    )
    report = audit_research_library(root)
    assert report["ok"] is False
    assert any("fuente sin title" in error for error in report["errors"])


def test_audit_counts_traceable_literature_review(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    _write_dossier(root)
    report = audit_research_library(root)
    assert report["ok"] is True
    assert report["literature_review_count"] == 1
    assert report["traceable_literature_reviews"] == 1
    assert report["unique_source_ids_referenced_by_dossiers"] == 1


def test_audit_rejects_unknown_source_reference(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    _write_dossier(root, "UNKNOWN-SOURCE")
    report = audit_research_library(root)
    assert report["ok"] is True
    assert report["traceable_literature_reviews"] == 0
    assert any("ID de fuente no registrado" in error for error in report["areas"][0]["literature_review_errors"])


def test_audit_requires_https_source_urls(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    registry_path = root / "knowledge/research/source_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["sources"][0]["url"] = "http://example.org/source"
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    report = audit_research_library(root)
    assert report["ok"] is False
    assert any("HTTPS" in error for error in report["errors"])
