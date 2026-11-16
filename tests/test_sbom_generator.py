import tempfile
import unittest
from pathlib import Path

from sbom_generator import LockfileError, build_sbom


class SbomGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "requirements.txt").write_text("Requests==2.34.2\n", encoding="utf-8")
        (self.root / "requirements.lock").write_text(
            "-r requirements.txt\ncertifi==2026.10.23\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_generates_deterministic_cyclonedx_with_direct_and_transitive_scope(self):
        first = build_sbom(self.root)
        second = build_sbom(self.root)
        self.assertEqual(first, second)
        self.assertEqual(first["bomFormat"], "CycloneDX")
        self.assertEqual(first["specVersion"], "1.5")
        by_name = {item["name"]: item for item in first["components"]}
        self.assertEqual(by_name["requests"]["properties"][0]["value"], "direct")
        self.assertEqual(by_name["certifi"]["properties"][0]["value"], "transitive")

    def test_rejects_unpinned_dependency(self):
        (self.root / "requirements.lock").write_text("requests>=2.0\n", encoding="utf-8")
        with self.assertRaises(LockfileError):
            build_sbom(self.root)

    def test_rejects_traversal_include(self):
        (self.root / "requirements.lock").write_text("-r ../outside.txt\n", encoding="utf-8")
        with self.assertRaises(LockfileError):
            build_sbom(self.root)

    def test_rejects_missing_direct_dependency_from_lock(self):
        (self.root / "requirements.lock").write_text("certifi==2026.10.23\n", encoding="utf-8")
        with self.assertRaises(LockfileError):
            build_sbom(self.root)


if __name__ == "__main__":
    unittest.main()
