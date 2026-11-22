import hashlib
import io
import tempfile
import unittest
from contextlib import redirect_stderr
import zipfile
from pathlib import Path
from unittest.mock import patch

import dependency_artifact_manifest
from dependency_artifact_manifest import ArtifactManifestError, build_manifest


class DependencyArtifactManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.wheelhouse = self.root / "wheelhouse"
        self.wheelhouse.mkdir()
        self.write_lock("a" * 64, "b" * 64)

    def write_lock(self, requests_hash, certifi_hash):
        newline = chr(10)
        slash = chr(92)
        (self.root / "requirements.txt").write_text(
            "requests==2.0 " + slash + newline
            + "    --hash=sha256:" + requests_hash + newline,
            encoding="utf-8",
        )
        (self.root / "requirements.lock").write_text(
            "-r requirements.txt" + newline
            + "certifi==1.0 " + slash + newline
            + "    --hash=sha256:" + certifi_hash + newline,
            encoding="utf-8",
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

    def pin_created_wheels(self, requests_wheel=None, certifi_wheel=None):
        requests_hash = (
            hashlib.sha256(requests_wheel.read_bytes()).hexdigest()
            if requests_wheel else "a" * 64
        )
        certifi_hash = (
            hashlib.sha256(certifi_wheel.read_bytes()).hexdigest()
            if certifi_wheel else "b" * 64
        )
        self.write_lock(requests_hash, certifi_hash)

    def test_manifest_hashes_exact_locked_wheels_and_binds_lock_hash(self):
        requests_wheel = self.wheel("requests-2.0-py3-none-any.whl", "requests", "2.0")
        certifi_wheel = self.wheel("certifi-1.0-py3-none-any.whl", "certifi", "1.0")
        self.pin_created_wheels(requests_wheel, certifi_wheel)
        result = build_manifest(self.root, self.wheelhouse)
        self.assertEqual(len(result["artifacts"]), 2)
        self.assertEqual(
            {item["name"] for item in result["artifacts"]},
            {"requests", "certifi"},
        )
        self.assertTrue(all(len(item["sha256"]) == 64 for item in result["artifacts"]))
        self.assertEqual(len(result["lock_sha256"]), 64)
        self.assertIn("verificados contra hashes", result["scope"])

    def test_manifest_rejects_wheel_hash_not_pinned(self):
        self.wheel("requests-2.0-py3-none-any.whl", "requests", "2.0")
        self.wheel("certifi-1.0-py3-none-any.whl", "certifi", "1.0")
        with self.assertRaisesRegex(ArtifactManifestError, "no coincide con requirements.lock"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_supports_a_secondary_lock_path(self):
        sandbox = self.root / "sandbox"
        sandbox.mkdir()
        wheelhouse = self.root / "sandbox-wheelhouse"
        wheelhouse.mkdir()
        first = self.wheel("ruff-0.14.5-py3-none-any.whl", "ruff", "0.14.5")
        second = self.wheel("bandit-1.8.6-py3-none-any.whl", "bandit", "1.8.6")
        (sandbox / "requirements.lock").write_text(
            "bandit==1.8.6 --hash=sha256:"
            + hashlib.sha256(second.read_bytes()).hexdigest() + chr(10)
            + "ruff==0.14.5 --hash=sha256:"
            + hashlib.sha256(first.read_bytes()).hexdigest() + chr(10),
            encoding="utf-8",
        )
        for item in (first, second):
            (wheelhouse / item.name).write_bytes(item.read_bytes())
        result = build_manifest(
            self.root, wheelhouse, lock_file="sandbox/requirements.lock"
        )
        self.assertEqual(result["lock_file"], "sandbox/requirements.lock")
        self.assertEqual(len(result["artifacts"]), 2)

    def test_manifest_rejects_missing_locked_wheel(self):
        requests_wheel = self.wheel("requests-2.0-py3-none-any.whl", "requests", "2.0")
        self.pin_created_wheels(requests_wheel=requests_wheel)
        with self.assertRaisesRegex(ArtifactManifestError, "certifi"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_version_not_in_lock(self):
        requests_wheel = self.wheel("requests-9.9-py3-none-any.whl", "requests", "9.9")
        certifi_wheel = self.wheel("certifi-1.0-py3-none-any.whl", "certifi", "1.0")
        self.pin_created_wheels(requests_wheel, certifi_wheel)
        with self.assertRaisesRegex(ArtifactManifestError, "versión distinta"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_oversized_wheel_metadata(self):
        path = self.wheelhouse / "requests-2.0-py3-none-any.whl"
        metadata = (
            "Metadata-Version: 2.1\\nName: requests\\nVersion: 2.0\\n\\n"
            + "x" * (2 * 1024 * 1024 + 1)
        )
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("requests-2.0.dist-info/METADATA", metadata)
        with self.assertRaisesRegex(ArtifactManifestError, "METADATA supera 2 MiB"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_invalid_wheel(self):
        (self.wheelhouse / "broken.whl").write_bytes(b"not a zip")
        with self.assertRaisesRegex(ArtifactManifestError, "Wheel inválido"):
            build_manifest(self.root, self.wheelhouse)


    def test_manifest_rejects_metadata_version_line_injection(self):
        requests = self.wheelhouse / "requests-2.0-py3-none-any.whl"
        with zipfile.ZipFile(requests, "w") as archive:
            archive.writestr(
                "requests-2.0.dist-info/METADATA",
                "Metadata-Version: 2.1" + chr(10)
                + "Name: requests" + chr(10)
                + "Version: 2.0" + chr(10)
                + " injected: lock-line" + chr(10),
            )
        certifi = self.wheel(
            "certifi-1.0-py3-none-any.whl", "certifi", "1.0"
        )
        self.pin_created_wheels(requests, certifi)
        with self.assertRaisesRegex(ArtifactManifestError, "Name/Version inválidos"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_duplicate_identity_headers(self):
        requests = self.wheelhouse / "requests-2.0-py3-none-any.whl"
        with zipfile.ZipFile(requests, "w") as archive:
            archive.writestr(
                "requests-2.0.dist-info/METADATA",
                "Metadata-Version: 2.1" + chr(10)
                + "Name: requests" + chr(10)
                + "Name: attacker" + chr(10)
                + "Version: 2.0" + chr(10),
            )
        certifi = self.wheel(
            "certifi-1.0-py3-none-any.whl", "certifi", "1.0"
        )
        self.pin_created_wheels(requests, certifi)
        with self.assertRaisesRegex(ArtifactManifestError, "identidad METADATA"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_oversized_wheel_before_metadata_read(self):
        (self.wheelhouse / "large.whl").write_bytes(b"x" * 9)
        with patch("dependency_artifact_manifest.MAX_WHEEL_BYTES", 8):
            with self.assertRaisesRegex(ArtifactManifestError, "supera el límite"):
                build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_wheelhouse_count_limit(self):
        (self.wheelhouse / "one.whl").write_bytes(b"x")
        (self.wheelhouse / "two.whl").write_bytes(b"x")
        with patch("dependency_artifact_manifest.MAX_WHEEL_COUNT", 1):
            with self.assertRaisesRegex(ArtifactManifestError, "límite de 1 wheels"):
                build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_total_wheelhouse_size_limit(self):
        (self.wheelhouse / "one.whl").write_bytes(b"x")
        (self.wheelhouse / "two.whl").write_bytes(b"x")
        with patch("dependency_artifact_manifest.MAX_WHEELHOUSE_BYTES", 1):
            with self.assertRaisesRegex(ArtifactManifestError, "límite total"):
                build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_symlink_wheel(self):
        target = self.root / "outside.whl"
        with zipfile.ZipFile(target, "w") as archive:
            archive.writestr(
                "requests-2.0.dist-info/METADATA",
                "Metadata-Version: 2.1" + chr(10)
                + "Name: requests" + chr(10)
                + "Version: 2.0" + chr(10),
            )
        (self.wheelhouse / "requests.whl").symlink_to(target)
        with self.assertRaisesRegex(ArtifactManifestError, "symlinks"):
            build_manifest(self.root, self.wheelhouse)

    def test_manifest_rejects_symlink_wheelhouse(self):
        link = self.root / "wheelhouse-link"
        link.symlink_to(self.wheelhouse, target_is_directory=True)
        with self.assertRaisesRegex(ArtifactManifestError, "directorio real"):
            build_manifest(self.root, link)


    def test_cli_redacts_manifest_errors(self):
        secret = "artifact-cli-secret"
        output = io.StringIO()
        with patch(
            "sys.argv",
            ["dependency_artifact_manifest.py", "--wheelhouse", str(self.wheelhouse), "--output", str(self.root / "manifest.json")],
        ), patch.object(
            dependency_artifact_manifest, "build_manifest",
            side_effect=ArtifactManifestError(f"invalid token={secret}"),
        ), redirect_stderr(output):
            result = dependency_artifact_manifest.main()
        self.assertEqual(result, 2)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())

if __name__ == "__main__":
    unittest.main()
