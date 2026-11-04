"""Pruebas del motor controlado de experimentos."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
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

    def test_plan_does_not_execute_or_persist(self):
        with (
            patch.object(engine.subprocess, "run") as fake_run,
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
        def fake_run(command, cwd, stdout, stderr, timeout, check):
            stdout.write(b"1 passed in 0.01s\n")
            return SimpleNamespace(returncode=0)

        with patch.object(engine.subprocess, "run", side_effect=fake_run):
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
        def fake_run(command, cwd, stdout, stderr, timeout, check):
            stdout.write(b"1 failed\n")
            return SimpleNamespace(returncode=1)

        with patch.object(engine.subprocess, "run", side_effect=fake_run):
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
        def fake_run(command, cwd, stdout, stderr, timeout, check):
            raise subprocess.TimeoutExpired(command, timeout)

        with patch.object(engine.subprocess, "run", side_effect=fake_run):
            report = engine.run_experiment(
                hypothesis="La prueba puede terminar dentro del límite.",
                test_path="tests/test_sample.py",
                timeout=1,
                execute=True,
            )

        self.assertEqual(report["status"], "timeout")
        self.assertIn("inconcluso", report["outcome_interpretation"])
        self.assertIsNone(report["return_code"])


if __name__ == "__main__":
    unittest.main()
