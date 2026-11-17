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
        (self.root / "requirements.txt").write_text("requests==2.0\n", encoding="utf-8")
        (self.root / "requirements.lock").write_text(
            "-r requirements.txt\ncertifi==1.0\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def wheel(self, filename, name, version):
        path = self.wheelhouse / filename
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(
                f"{name}-{version}.dist-info/METADATA",
                f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n",
            )
        return path

    def test_manifest_hashes_exact_locked_wheels_and_binds_lock_hash(self):
        self.wheel("requests-2.0-py3-none-any.whl", "requests", "2.0")
        self.wheel("certifi-1.0-py3-none-any.whl", "certifi", "1.0")
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
        self.wheel("requests-2.0-py3-none-any.whl", "requests", "2.0")
        with self.assertRaisesRegex(ArtifactManifestError, "certifi"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_version_not_in_lock(self):
        self.wheel("requests-9.9-py3-none-any.whl", "requests", "9.9")
        self.wheel("certifi-1.0-py3-none-any.whl", "certifi", "1.0")
        with self.assertRaisesRegex(ArtifactManifestError, "versión distinta"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_invalid_wheel(self):
        (self.wheelhouse / "broken.whl").write_bytes(b"not a zip")
        with self.assertRaisesRegex(ArtifactManifestError, "Wheel inválido"):
            build_manifest(self.root, self.wheelhouse)


if __name__ == "__main__":
    unittest.main()
