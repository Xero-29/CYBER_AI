import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from sbom_generator import LockfileError, build_sbom


class SbomGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        newline = chr(10)
        slash = chr(92)
        (self.root / "requirements.txt").write_text(
            "Requests==2.34.2 " + slash + newline
            + "    --hash=sha256:" + "a" * 64 + newline,
            encoding="utf-8",
        )
        (self.root / "requirements.lock").write_text(
            "-r requirements.txt" + newline
            + "certifi==2026.10.23 " + slash + newline
            + "    --hash=sha256:" + "b" * 64 + newline,
            encoding="utf-8",
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

    def test_includes_platform_artifact_hashes_from_matching_manifest(self):
        manifest_path = self.root / "artifacts.json"
        lock_hash = hashlib.sha256(
            (self.root / "requirements.lock").read_bytes()
        ).hexdigest()
        manifest_path.write_text(json.dumps({
            "lock_sha256": lock_hash,
            "artifacts": [
                {"name": "requests", "version": "2.34.2", "sha256": "a" * 64},
                {"name": "certifi", "version": "2026.10.23", "sha256": "b" * 64},
            ],
        }), encoding="utf-8")
        sbom = build_sbom(self.root, artifact_manifest=manifest_path)
        by_name = {item["name"]: item for item in sbom["components"]}
        self.assertEqual(by_name["requests"]["hashes"][0]["content"], "a" * 64)
        self.assertEqual(
            by_name["certifi"]["properties"][2]["value"], "b" * 64
        )

    def test_generates_sbom_for_secondary_locked_environment(self):
        sandbox = self.root / "sandbox"
        sandbox.mkdir()
        (sandbox / "requirements.in").write_text(
            "ruff==0.14.5" + chr(10) + "bandit==1.8.6" + chr(10),
            encoding="utf-8",
        )
        (sandbox / "requirements.lock").write_text(
            "bandit==1.8.6 --hash=sha256:" + "b" * 64 + chr(10)
            + "pygments==2.21.0 --hash=sha256:" + "c" * 64 + chr(10)
            + "ruff==0.14.5 --hash=sha256:" + "a" * 64 + chr(10),
            encoding="utf-8",
        )
        sbom = build_sbom(
            self.root,
            lock_file="sandbox/requirements.lock",
            direct_requirements="sandbox/requirements.in",
        )
        by_name = {item["name"]: item for item in sbom["components"]}
        self.assertEqual(by_name["ruff"]["properties"][0]["value"], "direct")
        self.assertEqual(by_name["bandit"]["properties"][0]["value"], "direct")
        self.assertEqual(by_name["pygments"]["properties"][0]["value"], "transitive")
        self.assertEqual(
            sbom["metadata"]["properties"][0]["value"], "sandbox/requirements.lock"
        )

    def test_rejects_artifact_manifest_for_different_lock(self):
        manifest_path = self.root / "artifacts.json"
        manifest_path.write_text(json.dumps({
            "lock_sha256": "0" * 64,
            "artifacts": [],
        }), encoding="utf-8")
        with self.assertRaisesRegex(LockfileError, "otro requirements.lock"):
            build_sbom(self.root, artifact_manifest=manifest_path)

    def test_rejects_incomplete_artifact_manifest(self):
        lock_hash = hashlib.sha256(
            (self.root / "requirements.lock").read_bytes()
        ).hexdigest()
        manifest_path = self.root / "artifacts.json"
        manifest_path.write_text(json.dumps({
            "lock_sha256": lock_hash,
            "artifacts": [
                {"name": "requests", "version": "2.34.2", "sha256": "a" * 64},
            ],
        }), encoding="utf-8")
        with self.assertRaisesRegex(LockfileError, "no cubre"):
            build_sbom(self.root, artifact_manifest=manifest_path)

    def test_rejects_unpinned_dependency(self):
        (self.root / "requirements.lock").write_text("requests>=2.0\n", encoding="utf-8")
        with self.assertRaises(LockfileError):
            build_sbom(self.root)

    def test_rejects_hashless_dependency(self):
        (self.root / "requirements.txt").write_text(
            "requests==2.34.2" + chr(10), encoding="utf-8"
        )
        with self.assertRaisesRegex(LockfileError, "sin hash SHA-256"):
            build_sbom(self.root)

    def test_rejects_artifact_hash_not_pinned_in_lock(self):
        lock_hash = hashlib.sha256((self.root / "requirements.lock").read_bytes()).hexdigest()
        manifest_path = self.root / "artifacts.json"
        manifest_path.write_text(json.dumps({
            "lock_sha256": lock_hash,
            "artifacts": [
                {"name": "requests", "version": "2.34.2", "sha256": "c" * 64},
                {"name": "certifi", "version": "2026.10.23", "sha256": "b" * 64},
            ],
        }), encoding="utf-8")
        with self.assertRaisesRegex(LockfileError, "no coincide"):
            build_sbom(self.root, artifact_manifest=manifest_path)

    def test_rejects_traversal_include(self):
        (self.root / "requirements.lock").write_text("-r ../outside.txt\n", encoding="utf-8")
        with self.assertRaises(LockfileError):
            build_sbom(self.root)

    def test_rejects_conflicting_versions_across_included_files(self):
        (self.root / "requirements.lock").write_text(
            "-r requirements.txt" + chr(10)
            + "requests==2.33.0 " + chr(92) + chr(10)
            + "    --hash=sha256:" + "c" * 64 + chr(10),
            encoding="utf-8",
        )
        with self.assertRaises(LockfileError):
            build_sbom(self.root)

    def test_rejects_missing_direct_dependency_from_lock(self):
        (self.root / "requirements.lock").write_text(
            "certifi==2026.10.23 " + chr(92) + chr(10)
            + "    --hash=sha256:" + "b" * 64 + chr(10),
            encoding="utf-8",
        )
        with self.assertRaises(LockfileError):
            build_sbom(self.root)


if __name__ == "__main__":
    unittest.main()
