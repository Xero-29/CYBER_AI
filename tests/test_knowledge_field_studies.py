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
    "identity",
    "malware",
    "forensics",
    "threat_intel",
    "reverse",
    "iot_hardware",
    "governance",
    "data_security",
    "machine_learning",
    "mathematics",
    "software_engineering",
    "soc_siem",
    "edr_xdr",
    "threat_hunting",
    "red_team",
    "wireless_security",
    "bug_bounty",
    "satellite_security",
    "physical_security",
    "email_dns_security",
    "fraud_abuse",
    "privacy_engineering",
    "cloud_forensics",
    "ai_red_team",
    "pki_hsm",
    "post_quantum_crypto",
    "business_continuity",
    "database_security",
    "vulnerability_research",
    "telecom_5g",
    "automotive_security",
    "hardware_security",
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


    def test_every_domain_maps_to_registered_sources(self):
        root = Path(__file__).resolve().parents[1]
        mapping = json.loads((root / "knowledge/research/field_studies/DOMAIN_SOURCE_MAP.json").read_text(encoding="utf-8"))
        registry = json.loads((root / "knowledge/research/source_registry.json").read_text(encoding="utf-8"))
        manifest = json.loads((root / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
        known_ids = {item["id"] for item in registry["sources"]}
        self.assertEqual(len(mapping["areas"]), manifest["area_count"])
        self.assertEqual({item["area_id"] for item in mapping["areas"]}, {item["id"] for item in manifest["areas"]})
        for area in mapping["areas"]:
            with self.subTest(area=area["area_id"]):
                self.assertGreaterEqual(len(area["source_ids"]), 2)
                self.assertEqual(len(area["source_ids"]), len(set(area["source_ids"])))
                self.assertTrue(set(area["source_ids"]).issubset(known_ids))


    def test_advanced_gap_register_covers_every_manifest_domain(self):
        gaps = json.loads(
            (ROOT / "knowledge/research/ADVANCED_GAP_REGISTER.json")
            .read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (ROOT / "knowledge/packs/manifest.json").read_text(encoding="utf-8")
        )
        entries = gaps["domains"]
        expected = {item["id"] for item in manifest["areas"]}
        actual = {item["domain_id"] for item in entries}
        self.assertEqual(len(entries), len(actual))
        self.assertEqual(actual, expected)
        for item in entries:
            with self.subTest(domain=item["domain_id"]):
                self.assertEqual(item["status"], "identified_not_yet_assessed")
                self.assertGreaterEqual(len(item["missing_advanced_topics"]), 4)
                self.assertEqual(len(item["missing_advanced_topics"]), len(set(item["missing_advanced_topics"])))

if __name__ == "__main__":
    unittest.main()
