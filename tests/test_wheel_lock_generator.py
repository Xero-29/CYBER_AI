import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from wheel_lock_generator import WheelLockError, build_lock


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


if __name__ == "__main__":
    unittest.main()
