import json
import tempfile
import unittest
from pathlib import Path

from core.plugin_registry import ManifestError, build_inventory, validate_manifest


class ComponentDiscoveryTests(unittest.TestCase):
    def manifest(self, component_id="example-plugin"):
        return {
            "manifest_version": 1,
            "id": component_id,
            "name": "Example",
            "version": "1.0.0",
            "kind": "analyzer",
            "capabilities": ["static_analysis"],
            "dependencies": [],
            "permissions": {
                "risk": "read_only",
                "requested": [],
                "requires_approval": False,
                "scope_required": False,
            },
            "enabled": True,
        }

    def test_valid_manifest_is_never_execution_authorized(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.component.json"
            result = validate_manifest(self.manifest(), path)
        self.assertEqual(result["trust_status"], "untrusted")
        self.assertFalse(result["execution_authorized"])

    def test_invalid_kind_is_rejected(self):
        data = self.manifest()
        data["kind"] = "arbitrary_code"
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ManifestError):
                validate_manifest(data, Path(directory) / "x.component.json")

    def test_discovery_builds_inventory_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "one.component.json").write_text(
                json.dumps(self.manifest()), encoding="utf-8"
            )
            inventory = build_inventory([root])
        self.assertEqual(inventory["component_count"], 1)
        self.assertFalse(inventory["components"][0]["execution_authorized"])
        self.assertEqual(inventory["errors"], [])

    def test_duplicate_ids_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("a", "b"):
                (root / f"{name}.component.json").write_text(
                    json.dumps(self.manifest()), encoding="utf-8"
                )
            inventory = build_inventory([root])
        self.assertEqual(inventory["component_count"], 1)
        self.assertEqual(len(inventory["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
