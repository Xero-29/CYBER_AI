import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from dependency_artifact_manifest import ArtifactManifestError, build_manifest


class DependencyArtifactManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.wheelhouse = self.root / "wheelhouse"
        self.wheelhouse.mkdir()
        requests = self.wheel("requests-2.0-py3-none-any.whl", "requests", "2.0")
        certifi = self.wheel("certifi-1.0-py3-none-any.whl", "certifi", "1.0")
        requests_hash = hashlib.sha256(requests.read_bytes()).hexdigest()
        certifi_hash = hashlib.sha256(certifi.read_bytes()).hexdigest()
        (self.root / "requirements.txt").write_text(
            "requests==2.0\ncertifi==1.0\n", encoding="utf-8"
        )
        (self.root / "requirements.lock").write_text(
            f"requests==2.0 --hash=sha256:{requests_hash}\n"
            f"certifi==1.0 --hash=sha256:{certifi_hash}\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def wheel(self, filename, name, version, *, extra_metadata=""):
        path = self.wheelhouse / filename
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(
                f"{name}-{version}.dist-info/METADATA",
                f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n"
                + extra_metadata,
            )
        return path

    def test_manifest_hashes_exact_locked_wheels_and_binds_lock_hash(self):
        result = build_manifest(self.root, self.wheelhouse)
        self.assertEqual(len(result["artifacts"]), 2)
        self.assertEqual(
            {item["name"] for item in result["artifacts"]},
            {"requests", "certifi"},
        )
        self.assertTrue(all(len(item["sha256"]) == 64 for item in result["artifacts"]))
        self.assertEqual(len(result["lock_sha256"]), 64)
        self.assertIn("no son hashes fijados", result["scope"])

    def test_manifest_rejects_missing_locked_wheel(self):
        (self.wheelhouse / "certifi-1.0-py3-none-any.whl").unlink()
        with self.assertRaisesRegex(ArtifactManifestError, "certifi"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_version_not_in_lock(self):
        (self.wheelhouse / "requests-2.0-py3-none-any.whl").unlink()
        self.wheel("requests-9.9-py3-none-any.whl", "requests", "9.9")
        with self.assertRaisesRegex(ArtifactManifestError, "versión distinta"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_oversized_wheel_metadata(self):
        path = self.wheelhouse / "requests-2.0-py3-none-any.whl"
        path.unlink()
        self.wheel(
            "requests-2.0-py3-none-any.whl",
            "requests",
            "2.0",
            extra_metadata="\n" + "x" * (2 * 1024 * 1024 + 1),
        )
        with self.assertRaisesRegex(ArtifactManifestError, "METADATA supera 2 MiB"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_invalid_wheel(self):
        (self.wheelhouse / "broken.whl").write_bytes(b"not a zip")
        with self.assertRaisesRegex(ArtifactManifestError, "Wheel inválido"):
            build_manifest(self.root, self.wheelhouse)


if __name__ == "__main__":
    unittest.main()
