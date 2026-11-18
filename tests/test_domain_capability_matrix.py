import unittest
from unittest.mock import patch

from domain_capability_matrix import (
    audit_domain_matrix,
    select_domain_capabilities,
)


class DomainCapabilityMatrixTests(unittest.TestCase):
    def test_every_offline_knowledge_pack_has_exactly_one_profile(self):
        result = audit_domain_matrix()
        self.assertEqual(result["manifest_area_count"], 48)
        self.assertEqual(result["profile_count"], 48)
        self.assertTrue(result["all_areas_mapped"])

    @patch("skillbook.search_skills", return_value=[])
    def test_network_task_links_knowledge_and_tool_candidates_without_execution(self, search_skills):
        result = select_domain_capabilities(
            "auditoría de red y análisis de PCAP",
            inventory={"tools": {}},
        )
        ids = {item["id"] for item in result["domains"]}
        self.assertIn("network", ids)
        network = next(item for item in result["domains"] if item["id"] == "network")
        self.assertEqual(
            {item["id"] for item in network["tool_candidates"]},
            {"tshark", "zeek", "nmap"},
        )
        self.assertTrue(all(
            not item["execution_permitted"]
            for item in network["tool_candidates"]
        ))
        self.assertFalse(result["execution_started"])

    @patch("skillbook.search_skills", return_value=[])
    def test_short_domain_terms_do_not_match_inside_unrelated_words(self, search_skills):
        result = select_domain_capabilities(
            "revisión de credenciales expuestas",
            inventory={"tools": {}},
        )
        self.assertNotIn("network", {item["id"] for item in result["domains"]})

    @patch("skillbook.search_skills", return_value=[])
    def test_catalog_only_domains_are_not_misreported_as_operational(self, search_skills):
        result = select_domain_capabilities(
            "seguridad móvil Android",
            inventory={"tools": {}},
        )
        mobile = next(item for item in result["domains"] if item["id"] == "mobile")
        self.assertTrue(mobile["tool_gap"])
        self.assertEqual(mobile["tool_candidates"], [])


if __name__ == "__main__":
    unittest.main()
