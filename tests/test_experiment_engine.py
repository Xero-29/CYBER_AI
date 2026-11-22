"""Pruebas del motor controlado de experimentos."""

import io
import json
import hashlib
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import compressed_store
import evidence_graph
import experiment_engine as engine
from compressed_evidence import read_evidence


class TestExperimentEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "tests").mkdir()
        (self.root / "data").mkdir()
        (self.root / "reports").mkdir()

        (self.root / "tests" / "test_sample.py").write_text(
            "def test_sample():\n    assert 1 + 1 == 2\n",
            encoding="utf-8",
        )

        self.old_project = engine.PROJECT
        self.old_graph_db = evidence_graph.DB_PATH
        self.old_compressed_db = compressed_store.DB_PATH

        engine.PROJECT = self.root
        evidence_graph.DB_PATH = self.root / "data" / "evidence.sqlite3"
        compressed_store.DB_PATH = self.root / "data" / "compressed.sqlite3"
        evidence_graph.initialize()

    def tearDown(self):
        engine.PROJECT = self.old_project
        evidence_graph.DB_PATH = self.old_graph_db
        compressed_store.DB_PATH = self.old_compressed_db
        self.temp_dir.cleanup()


    def _process_result(self, *, stdout=b"", stderr=b"", returncode=0, timed_out=False):
        return {
            "returncode": returncode,
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "stdout_truncated": False,
            "stderr_truncated": False,
            "output_truncated": False,
            "timed_out": timed_out,
            "process_group_isolation_enforced": True,
            "process_tree_isolation_enforced": False,
        }

    def test_plan_does_not_execute_or_persist(self):
        with (
            patch.object(engine, "run_bounded_process") as fake_run,
            patch.object(evidence_graph, "create_session") as fake_session,
        ):
            plan = engine.run_experiment(
                hypothesis="La prueba de ejemplo debe pasar.",
                test_path="tests/test_sample.py",
            )

        self.assertEqual(plan["status"], "planned")
        self.assertFalse(plan["executed"])
        fake_run.assert_not_called()
        fake_session.assert_not_called()

    def test_rejects_path_outside_tests(self):
        with self.assertRaises(ValueError):
            engine.build_plan(
                "Hipótesis de prueba", "../agent_runner.py"
            )

    def test_rejects_invalid_timeout(self):
        with self.assertRaises(ValueError):
            engine.build_plan(
                "Hipótesis de prueba",
                "tests/test_sample.py",
                timeout=0,
            )

    def test_success_records_evidence_and_links_hypothesis(self):
        def fake_run(command, cwd, env, timeout, max_output_bytes, capture_tail):
            self.assertNotIn("CYBER_AI_EXPERIMENT_SECRET", env)
            return self._process_result(stdout=b"1 passed in 0.01s\n")

        with patch.dict(os.environ, {"CYBER_AI_EXPERIMENT_SECRET": "do-not-inherit"}):
            with patch.object(engine, "run_bounded_process", side_effect=fake_run):
            report = engine.run_experiment(
                hypothesis="La prueba de ejemplo pasa.",
                test_path="tests/test_sample.py",
                timeout=10,
                execute=True,
            )

        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["return_code"], 0)
        self.assertEqual(report["security_conclusion"], "not_determined_by_test_runner")
        self.assertTrue(report["stdout_sha256"])
        self.assertTrue(report["process_group_isolation_enforced"])
        self.assertFalse(report["process_tree_isolation_enforced"])
        self.assertEqual(report["execution_environment"], "minimal_without_application_secrets")
        self.assertTrue(report["evidence_node_id"])
        self.assertTrue(report["hypothesis_node_id"])
        self.assertTrue(report["evidence_edge_id"])

        counts = evidence_graph.counts()
        self.assertEqual(counts["nodes"], 2)
        self.assertEqual(counts["edges"], 1)

        saved = read_evidence(
            report["evidence_node_id"],
            report["session_id"],
        )
        saved_report = json.loads(saved["content"])
        self.assertEqual(saved_report["status"], "passed")

        report_path = self.root / report["report_path"]
        self.assertTrue(report_path.is_file())

    def test_failed_test_is_not_called_a_confirmed_vulnerability(self):
        def fake_run(command, cwd, env, timeout, max_output_bytes, capture_tail):
            return self._process_result(stdout=b"1 failed\n", returncode=1)

        with patch.object(engine, "run_bounded_process", side_effect=fake_run):
            report = engine.run_experiment(
                hypothesis="Una prueba de ejemplo podría fallar.",
                test_path="tests/test_sample.py",
                timeout=10,
                execute=True,
            )

        self.assertEqual(report["status"], "failed")
        self.assertIn(
            "no demuestra por sí solo una vulnerabilidad",
            report["outcome_interpretation"],
        )
        self.assertEqual(report["security_conclusion"], "not_determined_by_test_runner")

    def test_timeout_is_recorded_as_inconclusive(self):
        def fake_run(command, cwd, env, timeout, max_output_bytes, capture_tail):
            return self._process_result(returncode=-9, timed_out=True)

        with patch.object(engine, "run_bounded_process", side_effect=fake_run):
            report = engine.run_experiment(
                hypothesis="La prueba puede terminar dentro del límite.",
                test_path="tests/test_sample.py",
                timeout=1,
                execute=True,
            )

        self.assertEqual(report["status"], "timeout")
        self.assertIn("inconcluso", report["outcome_interpretation"])
        self.assertIsNone(report["return_code"])


    def test_experiment_redacts_output_and_writes_private_report(self):
        secret = "experiment-output-secret"

        def fake_run(command, cwd, env, timeout, max_output_bytes, capture_tail):
            return self._process_result(
                stdout=f"provider token={secret}\n".encode("utf-8"),
                stderr=f"password={secret}\n".encode("utf-8"),
            )

        with patch.object(engine, "run_bounded_process", side_effect=fake_run):
            report = engine.run_experiment(
                hypothesis="La salida de prueba debe quedar protegida.",
                test_path="tests/test_sample.py",
                timeout=10,
                execute=True,
            )

        self.assertNotIn(secret, report["stdout"])
        self.assertNotIn(secret, report["stderr"])
        self.assertIn("token=[REDACTED]", report["stdout"])
        self.assertIn("password=[REDACTED]", report["stderr"])
        report_path = self.root / report["report_path"]
        rendered = report_path.read_text(encoding="utf-8")
        self.assertNotIn(secret, rendered)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(report_path.stat().st_mode), 0o600)


    def test_execution_fails_closed_when_process_isolation_is_unavailable(self):
        from process_isolation import ProcessIsolationError

        with patch.object(
            engine, "run_bounded_process",
            side_effect=ProcessIsolationError("Job Objects no disponibles"),
        ):
            report = engine.run_experiment(
                hypothesis="La ejecución debe bloquearse sin aislamiento.",
                test_path="tests/test_sample.py",
                timeout=5,
                execute=True,
            )

        self.assertEqual(report["status"], "execution_error")
        self.assertFalse(report["process_group_isolation_enforced"])
        self.assertEqual(report["execution_environment"], "not_started")

    def test_cli_redacts_unexpected_errors(self):
        secret = "experiment-cli-secret"
        output = io.StringIO()
        with patch(
            "sys.argv",
            ["experiment_engine.py", "--hypothesis", "prueba", "--test", "tests/test_sample.py"],
        ), patch.object(
            engine, "run_experiment",
            side_effect=RuntimeError(f"falló el proceso token={secret}"),
        ), redirect_stderr(output):
            result = engine.main()
        self.assertEqual(result, 2)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())

if __name__ == "__main__":
    unittest.main()
