import json
import unittest
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "data" / "knowledge_sources" / "knowledge_catalog.json"


class KnowledgeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_area_and_resource_ids_are_unique(self):
        area_ids = [item["id"] for item in self.data["areas"]]
        resource_ids = [item["id"] for item in self.data["resources"]]
        self.assertEqual(len(area_ids), len(set(area_ids)))
        self.assertEqual(len(resource_ids), len(set(resource_ids)))

    def test_every_flat_resource_maps_to_an_area(self):
        area_ids = {item["id"] for item in self.data["areas"]}
        self.assertTrue(all(item["area_id"] in area_ids for item in self.data["resources"]))

    def test_new_knowledge_domains_exist(self):
        area_ids = {item["id"] for item in self.data["areas"]}
        self.assertTrue({"software_engineering", "machine_learning", "hardware_security", "mathematics"} <= area_ids)

    def test_expanded_security_specialties_exist(self):
        ids = {item["id"] for item in self.data["areas"]}
        self.assertTrue({"soc_siem", "edr_xdr", "threat_hunting", "red_team", "wireless_security", "ot_ics", "telecom_5g", "automotive_security", "satellite_security", "physical_security", "email_dns_security", "fraud_abuse", "privacy_engineering", "cloud_forensics", "ai_red_team", "pki_hsm", "post_quantum_crypto", "business_continuity", "database_security", "vulnerability_research"} <= ids)

    def test_catalog_references_are_not_misrepresented_as_downloaded(self):
        for item in self.data["resources"]:
            self.assertFalse(item["download"])
            self.assertFalse(item["verified_for_download"])
            self.assertEqual(item["license_status"], "pending")
            self.assertTrue(item["url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
