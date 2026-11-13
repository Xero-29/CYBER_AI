import json
import tempfile
import unittest
from pathlib import Path

import preflight


class PreflightTests(unittest.TestCase):
    def make_project(self, root):
        for relative in preflight.REQUIRED_FILES:
            path = root / relative
            if relative.endswith(".json"):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")
            elif relative == "tests":
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# fixture\n", encoding="utf-8")

    def test_ready_without_optional_tools_or_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            report = preflight.collect_checks(
                root=root,
                python_version=(3, 12, 0),
                module_lookup=lambda name: object() if name in preflight.REQUIRED_MODULES else None,
                executable_lookup=lambda name: None,
                environ={},
            )
        self.assertEqual(report["status"], "ready")
        self.assertGreater(report["warnings"], 0)
        self.assertFalse(report["network_accessed"])
        self.assertFalse(report["services_started"])

    def test_old_python_blocks_readiness(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            report = preflight.collect_checks(
                root=root,
                python_version=(3, 11, 9),
                module_lookup=lambda name: object(),
                executable_lookup=lambda name: None,
                environ={},
            )
        self.assertEqual(report["status"], "blocked")
        self.assertGreater(report["errors"], 0)


if __name__ == "__main__":
    unittest.main()
