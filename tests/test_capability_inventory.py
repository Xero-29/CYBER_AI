import unittest
from unittest.mock import patch

import capability_inventory


class CapabilityInventoryTests(unittest.TestCase):
    def test_catalog_contains_security_and_supply_chain_tools(self):
        ids = {item["id"] for item in capability_inventory.TOOL_CATALOG}
        self.assertTrue({"semgrep", "bandit", "pip_audit", "trivy", "syft", "gitleaks", "nmap", "nuclei"} <= ids)

    @patch("capability_inventory.shutil.which")
    def test_inventory_detects_presence_without_execution(self, which):
        which.side_effect = lambda name: f"/usr/bin/{name}" if name == "semgrep" else None
        result = capability_inventory.build_inventory()
        self.assertEqual(result["summary"]["registered"], len(capability_inventory.TOOL_CATALOG))
        self.assertTrue(result["tools"]["semgrep"]["available"])
        self.assertFalse(result["tools"]["nmap"]["available"])
        self.assertTrue(result["safety"]["discovery_only"])
        self.assertFalse(result["safety"]["executes_tools"])
        self.assertFalse(result["safety"]["tool_presence_grants_permission"])

    def test_active_network_tools_require_scoped_authorization(self):
        active = [
            item for item in capability_inventory.TOOL_CATALOG
            if item["risk"] == "active_network"
        ]
        self.assertTrue(active)
        self.assertTrue(all(
            item["execution_policy"] == "scoped_network_authorization"
            for item in active
        ))


if __name__ == "__main__":
    unittest.main()
