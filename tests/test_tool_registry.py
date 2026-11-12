import unittest

from tool_registry import select_tools


class ToolRegistryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = {
            "tools": {
                "semgrep": {"available": True, "path": "/usr/bin/semgrep"},
                "bandit": {"available": False, "path": None},
                "nmap": {"available": True, "path": "/usr/bin/nmap"},
                "nuclei": {"available": True, "path": "/usr/bin/nuclei"},
            }
        }

    def test_selects_local_code_review_tools(self):
        result = select_tools("analisis estatico de codigo Python", inventory=self.inventory)
        ids = {item["id"] for item in result["candidates"]}
        self.assertIn("semgrep", ids)
        self.assertIn("bandit", ids)
        self.assertTrue(all(not item["execution_permitted"] for item in result["candidates"]))

    def test_network_tools_are_candidates_not_authorized_actions(self):
        result = select_tools("descubrimiento de red y puertos", inventory=self.inventory)
        nmap = next(item for item in result["candidates"] if item["id"] == "nmap")
        self.assertTrue(nmap["authorization_required"])
        self.assertFalse(nmap["execution_permitted"])
        self.assertEqual(nmap["status"], "candidate_only")

    def test_empty_task_and_invalid_limit_are_rejected(self):
        with self.assertRaises(ValueError):
            select_tools(" ")
        with self.assertRaises(ValueError):
            select_tools("python", inventory=self.inventory, limit=0)


if __name__ == "__main__":
    unittest.main()
