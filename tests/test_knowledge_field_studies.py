from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDIES = {
    "network",
    "crypto",
    "ai_security",
    "ot_ics",
    "incident_response",
    "vuln_management",
    "devsecops",
    "secure_arch",
    "foundations",
    "appsec",
    "api",
    "linux",
    "windows_ad",
    "cloud",
    "containers",
    "mobile",
}


class KnowledgeFieldStudiesTests(unittest.TestCase):
    def test_each_initial_study_exists_and_is_linked(self) -> None:
        index_path = ROOT / "knowledge/research/field_studies/README.md"
        index = index_path.read_text(encoding="utf-8")
        for area in STUDIES:
            study = ROOT / "knowledge/deep_modules" / area / "RESEARCH_STUDY.md"
            self.assertTrue(study.is_file(), f"Missing field study: {area}")
            self.assertIn(f"../../deep_modules/{area}/RESEARCH_STUDY.md", index)

    def test_study_sources_are_registered_and_https(self) -> None:
        field_registry = json.loads(
            (ROOT / "knowledge/research/field_studies/SOURCE_REGISTER_2026-11-18.json")
            .read_text(encoding="utf-8")
        )
        central_registry = json.loads(
            (ROOT / "knowledge/research/source_registry.json")
            .read_text(encoding="utf-8")
        )
        field_sources = field_registry["sources"]
        central_ids = {item["id"] for item in central_registry["sources"]}
        field_ids = [item["id"] for item in field_sources]
        self.assertEqual(len(field_ids), len(set(field_ids)))
        for source in field_sources:
            self.assertTrue(source["url"].startswith("https://"), source["id"])
            self.assertIn(source["id"], central_ids, source["id"])
            self.assertTrue(source.get("verification_status"), source["id"])

    def test_research_index_links_protocol_and_source_register(self) -> None:
        index = (
            ROOT / "knowledge/research/field_studies/README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("../RESEARCH_PROTOCOL.md", index)
        self.assertIn("./SOURCE_REGISTER_2026-11-18.json", index)
        self.assertIn("no equivale a 48 dominios investigados", index)


if __name__ == "__main__":
    unittest.main()
