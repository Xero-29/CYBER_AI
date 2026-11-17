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
        self.assertEqual(result["safety"]["local_host_egress_isolation"], "not_enforced")
        self.assertTrue(result["safety"]["direct_execution_requires_explicit_execute"])
        self.assertFalse(result["tools"]["ruff"]["host_network_isolation_enforced"])
        self.assertTrue(result["tools"]["ruff"]["explicit_execute_required"])

    @patch("capability_inventory.subprocess.run")
    @patch("capability_inventory.shutil.which")
    def test_yara_and_tshark_availability_comes_from_isolated_docker_image(self, which, run):
        which.side_effect = lambda name: "/usr/bin/docker" if name == "docker" else None
        run.return_value = __import__("subprocess").CompletedProcess(
            ["docker"], 0, stdout="sha256:" + "a" * 64, stderr=""
        )
        result = capability_inventory.build_inventory()
        self.assertTrue(result["tools"]["yara"]["available"])
        self.assertTrue(result["tools"]["tshark"]["available"])
        self.assertEqual(result["tools"]["yara"]["path"], "docker-image:sha256:" + "a" * 64)
        self.assertTrue(result["tools"]["yara"]["host_network_isolation_enforced"])
        self.assertEqual(
            result["safety"]["local_host_egress_isolation"],
            "docker_network_none_for_yara_tshark_only",
        )

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



    def test_inventory_reports_adapter_coverage_separately_from_installation(self):
        result = capability_inventory.build_inventory()
        self.assertEqual(
            result["summary"]["adapter_registered"],
            sum(item["id"] in capability_inventory.TOOL_SPECS for item in capability_inventory.TOOL_CATALOG),
        )
        self.assertEqual(
            result["summary"]["catalog_only"],
            result["summary"]["registered"] - result["summary"]["adapter_registered"],
        )
        self.assertIn("adapter_registered", result["tools"]["ruff"])

if __name__ == "__main__":
    unittest.main()
