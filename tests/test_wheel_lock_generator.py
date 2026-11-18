import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

import wheel_lock_generator

from unittest.mock import patch

from wheel_lock_generator import WheelLockError, build_lock, wheel_metadata


class WheelLockGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.wheelhouse = self.root / "wheelhouse"
        self.wheelhouse.mkdir()
        self.requirements = self.root / "requirements.in"
        self.requirements.write_text(
            "ruff==0.14.5" + chr(10) + "bandit==1.8.6" + chr(10),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def wheel(self, filename, name, version):
        path = self.wheelhouse / filename
        metadata = (
            "Metadata-Version: 2.1" + chr(10)
            + f"Name: {name}" + chr(10)
            + f"Version: {version}" + chr(10)
        )
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(f"{name}-{version}.dist-info/METADATA", metadata)
        return path

    def test_builds_sorted_lock_with_verified_wheel_hashes(self):
        ruff = self.wheel("ruff-0.14.5-py3-none-any.whl", "ruff", "0.14.5")
        bandit = self.wheel("bandit-1.8.6-py3-none-any.whl", "bandit", "1.8.6")
        lock = build_lock(self.wheelhouse, self.requirements)
        self.assertLess(lock.index("bandit=="), lock.index("ruff=="))
        self.assertIn(hashlib.sha256(ruff.read_bytes()).hexdigest(), lock)
        self.assertIn(hashlib.sha256(bandit.read_bytes()).hexdigest(), lock)
        self.assertEqual(lock, build_lock(self.wheelhouse, self.requirements))

    def test_rejects_missing_direct_wheel(self):
        self.wheel("ruff-0.14.5-py3-none-any.whl", "ruff", "0.14.5")
        with self.assertRaisesRegex(WheelLockError, "bandit"):
            build_lock(self.wheelhouse, self.requirements)

    def test_rejects_conflicting_versions(self):
        self.wheel("ruff-0.14.5-py3-none-any.whl", "ruff", "0.14.5")
        self.wheel("ruff-0.14.4-py3-none-any.whl", "ruff", "0.14.4")
        self.wheel("bandit-1.8.6-py3-none-any.whl", "bandit", "1.8.6")
        with self.assertRaisesRegex(WheelLockError, "Versiones múltiples"):
            build_lock(self.wheelhouse, self.requirements)

    def test_rejects_oversized_wheel_metadata(self):
        path = self.wheelhouse / "ruff-0.14.5-py3-none-any.whl"
        metadata = (
            "Metadata-Version: 2.1\\nName: ruff\\nVersion: 0.14.5\\n\\n"
            + "x" * (2 * 1024 * 1024 + 1)
        )
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("ruff-0.14.5.dist-info/METADATA", metadata)
        with self.assertRaisesRegex(WheelLockError, "METADATA supera 2 MiB"):
            build_lock(self.wheelhouse, self.requirements)

    def test_rejects_invalid_wheel(self):
        (self.wheelhouse / "broken.whl").write_bytes(b"not a wheel")
        with self.assertRaisesRegex(WheelLockError, "Wheel inválido"):
            build_lock(self.wheelhouse, self.requirements)

    def test_rejects_symlink_wheel(self):
        target = self.wheel("ruff-0.14.5-py3-none-any.whl", "ruff", "0.14.5")
        self.wheel("bandit-1.8.6-py3-none-any.whl", "bandit", "1.8.6")
        (self.wheelhouse / "ruff-copy.whl").symlink_to(target)
        with self.assertRaisesRegex(WheelLockError, "Wheel inseguro"):
            build_lock(self.wheelhouse, self.requirements)

    def test_rejects_unpinned_direct_requirement(self):
        self.requirements.write_text("ruff>=0.14.5" + chr(10), encoding="utf-8")
        with self.assertRaisesRegex(WheelLockError, "no fijado"):
            build_lock(self.wheelhouse, self.requirements)


    def test_rejects_wheel_metadata_version_line_injection(self):
        path = self.wheelhouse / "ruff-0.14.5-py3-none-any.whl"
        metadata = (
            "Metadata-Version: 2.1" + chr(10)
            + "Name: ruff" + chr(10)
            + "Version: 0.14.5" + chr(10)
            + " injected: lock-line" + chr(10)
        )
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("ruff-0.14.5.dist-info/METADATA", metadata)
        with self.assertRaisesRegex(WheelLockError, "Name/Version inválidos"):
            wheel_metadata(path)

    def test_rejects_duplicate_wheel_identity_headers(self):
        path = self.wheelhouse / "ruff-0.14.5-py3-none-any.whl"
        metadata = (
            "Metadata-Version: 2.1" + chr(10)
            + "Name: ruff" + chr(10)
            + "Name: attacker" + chr(10)
            + "Version: 0.14.5" + chr(10)
        )
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("ruff-0.14.5.dist-info/METADATA", metadata)
        with self.assertRaisesRegex(WheelLockError, "identidad METADATA"):
            wheel_metadata(path)

    def test_rejects_oversized_wheel_before_opening_archive(self):
        path = self.wheelhouse / "large.whl"
        path.write_bytes(b"x" * 9)
        with patch("wheel_lock_generator.MAX_WHEEL_BYTES", 8):
            with self.assertRaisesRegex(WheelLockError, "supera el límite"):
                wheel_metadata(path)

    def test_rejects_wheelhouse_count_limit_before_parsing(self):
        (self.wheelhouse / "one.whl").write_bytes(b"x")
        (self.wheelhouse / "two.whl").write_bytes(b"x")
        with patch("wheel_lock_generator.MAX_WHEEL_COUNT", 1):
            with self.assertRaisesRegex(WheelLockError, "límite de 1 wheels"):
                build_lock(self.wheelhouse, self.requirements)

    def test_rejects_total_wheelhouse_size_limit(self):
        (self.wheelhouse / "one.whl").write_bytes(b"x")
        (self.wheelhouse / "two.whl").write_bytes(b"x")
        with patch("wheel_lock_generator.MAX_WHEELHOUSE_BYTES", 1):
            with self.assertRaisesRegex(WheelLockError, "límite total"):
                build_lock(self.wheelhouse, self.requirements)

    def test_rejects_oversized_requirements_file_with_bounded_read(self):
        self.requirements.write_text("ruff==0.14.5" + chr(10), encoding="utf-8")
        with patch("wheel_lock_generator.MAX_REQUIREMENTS_BYTES", 4):
            with self.assertRaisesRegex(WheelLockError, "supera 4 bytes"):
                build_lock(self.wheelhouse, self.requirements)

    def test_rejects_symlink_requirements_file(self):
        target = self.root / "actual-requirements.in"
        target.write_text("ruff==0.14.5" + chr(10), encoding="utf-8")
        link = self.root / "linked-requirements.in"
        link.symlink_to(target)
        with self.assertRaisesRegex(WheelLockError, "inexistente o inseguro"):
            build_lock(self.wheelhouse, link)



    def test_main_reports_symlink_output_as_error(self):
        target = self.root / "target.lock"
        target.write_text("keep", encoding="utf-8")
        output = self.root / "output.lock"
        try:
            output.symlink_to(target)
        except OSError:
            self.skipTest("symlinks unavailable")
        with patch.object(wheel_lock_generator, "build_lock", return_value="lock"):
            self.assertEqual(
                wheel_lock_generator.main([
                    "--wheelhouse", str(self.wheelhouse),
                    "--requirements", str(self.requirements),
                    "--output", str(output),
                ]),
                2,
            )
        self.assertEqual(target.read_text(encoding="utf-8"), "keep")

if __name__ == "__main__":
    unittest.main()
