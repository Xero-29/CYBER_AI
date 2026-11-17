"""Structural crosswalk audit; it does not certify semantic or exhaustive coverage."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def audit(root: Path = ROOT) -> dict:
    errors, warnings = [], []
    try:
        matrix = json.loads((root / "knowledge/research/global_coverage_matrix.json").read_text(encoding="utf-8"))
        manifest = json.loads((root / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "area_count": 0, "reference_count": 0}
    manifest_ids = [x.get("id") for x in manifest.get("areas", [])]
    area_rows = matrix.get("areas", [])
    area_ids = [x.get("id") for x in area_rows]
    refs = matrix.get("references", [])
    ref_ids = [x.get("id") for x in refs]
    if len(manifest_ids) != len(set(manifest_ids)): errors.append("IDs duplicados en manifiesto")
    if len(area_ids) != len(set(area_ids)): errors.append("IDs duplicados en matriz")
    if len(ref_ids) != len(set(ref_ids)): errors.append("IDs duplicados en referencias")
    if set(manifest_ids) != set(area_ids): errors.append("La matriz no coincide exactamente con el manifiesto")
    known_refs = set(ref_ids)
    for ref in refs:
        for key in ("id", "title", "publisher", "type", "scope", "domains", "verification_status"):
            if not ref.get(key): errors.append(f"Referencia sin {key}: {ref.get('id', '?')}")
        unknown = set(ref.get("domains", [])) - set(manifest_ids)
        if unknown: errors.append(f"{ref.get('id')}: dominios inexistentes {sorted(unknown)}")
    reference_domains = {item["id"]: set(item.get("domains", [])) for item in refs}
    rows = []
    for area in area_rows:
        aid, links = area.get("id", "?"), area.get("reference_ids", [])
        unknown = sorted(set(links) - known_refs)
        if unknown: errors.append(f"{aid}: referencias inexistentes {unknown}")
        inconsistent = sorted(ref_id for ref_id in links if ref_id in reference_domains and aid not in reference_domains[ref_id])
        if inconsistent: errors.append(f"{aid}: mapeo inverso ausente en referencias {inconsistent}")
        if len(links) != len(set(links)): errors.append(f"{aid}: referencias duplicadas")
        if not links: warnings.append(f"{aid}: sin referencias asociadas")
        rows.append({"id": aid, "reference_count": len(links), "references_exist": not unknown,
                     "coverage_status": area.get("coverage_status"),
                     "content_depth_status": area.get("content_depth_status"),
                     "known_gaps": area.get("known_gaps", [])})
    mapped = sum(x["reference_count"] > 0 for x in rows)
    return {"ok": not errors, "errors": errors, "warnings": warnings, "area_count": len(rows),
            "areas_with_reference_mapping": mapped, "areas_without_reference_mapping": len(rows)-mapped,
            "reference_count": len(refs), "cross_cutting_gap_count": len(matrix.get("cross_cutting_gaps", [])),
            "content_depth_assessed": 0, "exhaustive_coverage_claim": False, "areas": rows,
            "limitations": ["A mapping is not proof that a pack covers a reference.",
                "Full texts, legal applicability, tool operation and lab execution are not assessed.",
                "The reference set is curated and non-exhaustive.",
                "No total coverage percentage is calculated without a complete weighted universe."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Áreas auditadas: {report['area_count']}")
        print(f"Áreas con referencias asociadas: {report['areas_with_reference_mapping']}")
        print(f"Áreas sin referencias asociadas: {report['areas_without_reference_mapping']}")
        print(f"Familias de referencia: {report['reference_count']}")
        print(f"Brechas transversales: {report['cross_cutting_gap_count']}")
        print(f"Profundidad evaluada: {report['content_depth_assessed']}")
        print("Cobertura exhaustiva demostrada: no")
        for row in report["areas"]:
            if row["reference_count"] < 2: print(f"- Revisar {row['id']}: {row['reference_count']} referencias")
        for error in report["errors"]: print("ERROR:", error)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
