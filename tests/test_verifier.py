import unittest
from pathlib import Path


class TestCyberAI(unittest.TestCase):
    def test_project_directories_exist(self):
        for name in ("reports", "data", "tests"):
            with self.subTest(directory=name):
                self.assertTrue(Path(name).is_dir())

    def test_preflight_entrypoint_exists(self):
        self.assertTrue(Path("preflight.py").is_file())

    def test_verification_script_exists(self):
        self.assertTrue(Path("verify.sh").is_file())

    def test_context_exists(self):
        self.assertTrue(Path("CONTEXT.md").is_file())


if __name__ == "__main__":
    unittest.main()
