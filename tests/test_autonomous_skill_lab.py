import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import autonomous_skill_lab as lab


class AutonomousSkillLabTests(unittest.TestCase):
    def valid_files(self):
        return {
            "Cargo.toml": '[package]\nname = "safe-lab"\nversion = "0.1.0"\nedition = "2021"\n',
            "src/main.rs": '#[test]\nfn arithmetic_is_checked() { assert_eq!(2usize.checked_add(2), Some(4)); }\nfn main() {}\n',
        }

    def test_json_must_be_object(self):
        with self.assertRaises(lab.LabError):
            lab._json_object('["not", "an", "object"]')

    def test_accepts_minimal_dependency_free_rust_project(self):
        result = lab.validate_generated_files(self.valid_files())
        self.assertIn("Cargo.toml", result)
        self.assertIn("src/main.rs", result)

    def test_rejects_path_traversal_and_unapproved_files(self):
        files = self.valid_files()
        files["../../outside.txt"] = "no"
        with self.assertRaisesRegex(lab.LabError, "allowlist"):
            lab.validate_generated_files(files)

    def test_rejects_dependencies_and_build_scripts(self):
        for addition in (
            '\n[dependencies]\nserde = "1"\n',
            '\nbuild = "build.rs"\n',
        ):
            files = self.valid_files()
            files["Cargo.toml"] += addition
            with self.subTest(addition=addition), self.assertRaises(lab.LabError):
                lab.validate_generated_files(files)

    def test_rejects_oversized_or_empty_files(self):
        files = self.valid_files()
        files["src/main.rs"] = "x" * (lab.MAX_FILE_BYTES + 1)
        with self.assertRaisesRegex(lab.LabError, "grande"):
            lab.validate_generated_files(files)
        files["src/main.rs"] = ""
        with self.assertRaises(lab.LabError):
            lab.validate_generated_files(files)

    def test_docker_command_has_isolation_and_no_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = lab.build_docker_command(tmp, timeout=90)
        for flag in ("--network=none", "--read-only", "--cap-drop=ALL",
                     "--security-opt=no-new-privileges:true", "--pids-limit=96",
                     "--memory=1g", "--cpus=2", "--user=65532:65532"):
            self.assertIn(flag, command)
        self.assertIn("CARGO_NET_OFFLINE=true", command)
        self.assertEqual(command[-5:], ["cargo", "test", "--offline", "--manifest-path", "/workspace/Cargo.toml"])

    def test_docker_command_rejects_bad_timeout_and_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(lab.LabError):
                lab.build_docker_command(tmp, timeout=0)
            with self.assertRaises(lab.LabError):
                lab.build_docker_command(tmp, image="bad image")

    def test_ollama_url_is_loopback_only(self):
        with patch.object(lab.urllib.request, "urlopen") as open_url:
            with self.assertRaisesRegex(lab.LabError, "loopback"):
                lab.ollama_chat("model", [], base_url="http://example.com:11434")
            open_url.assert_not_called()

    def test_learning_cycle_retries_and_keeps_skill_as_candidate(self):
        plan = {"objective": "safe demonstration"}
        execution = {
            "files": self.valid_files(),
            "procedure": ["write project", "cargo test"],
            "expected_result": "tests pass",
        }
        failed = {"status": "failed", "return_code": 101, "stderr": "test failed"}
        passed = {"status": "passed", "return_code": 0, "stdout": "1 passed"}
        with patch.object(lab, "_ask_json", side_effect=[plan, execution, plan, execution]), \
             patch.object(lab, "run_rust_lab", side_effect=[failed, passed]):
            result = lab.run_learning_cycle(
                "Prueba Rust", max_rounds=2, docker_bin="docker"
            )
        self.assertEqual(result["status"], "passed")
        self.assertEqual(len(result["attempts"]), 2)
        self.assertEqual(result["skill_candidate"]["status"], "candidate_only")

    def test_failed_or_inconclusive_execution_is_not_promoted(self):
        plan = {"objective": "safe demonstration"}
        execution = {"files": self.valid_files(), "procedure": [], "expected_result": ""}
        with patch.object(lab, "_ask_json", side_effect=[plan, execution]), \
             patch.object(lab, "run_rust_lab", return_value={"status": "failed"}):
            result = lab.run_learning_cycle("Prueba Rust", max_rounds=1)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["skill_candidate"]["status"], "not_eligible")


if __name__ == "__main__":
    unittest.main()
