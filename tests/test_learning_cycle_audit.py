import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import learning_cycle_audit
from execution_ledger import ExecutionLedger
import skillbook


class LearningCycleAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = ExecutionLedger(self.root / "ledger.sqlite3")
        self.db_patch = patch.object(skillbook, "DB_PATH", self.root / "skills.sqlite3")
        self.db_patch.start()
        self.memory_patch = patch.object(
            learning_cycle_audit.learning_memory,
            "MEMORY_FILE",
            self.root / "verified_lessons.jsonl",
        )
        self.memory_patch.start()
        self.path_patch = patch.object(
            learning_cycle_audit, "DEFAULT_DB", self.ledger.path
        )
        self.path_patch.start()
        self.ledger_patch = patch.object(
            learning_cycle_audit, "ExecutionLedger", return_value=self.ledger
        )
        self.ledger_patch.start()
        self.key_patch = patch.dict(
            os.environ, {learning_cycle_audit.learning_memory.APPROVAL_KEY_ENV: ""}
        )
        self.key_patch.start()

    def tearDown(self):
        self.key_patch.stop()
        self.ledger_patch.stop()
        self.path_patch.stop()
        self.memory_patch.stop()
        self.db_patch.stop()
        self.temp.cleanup()

    def test_empty_cycle_is_audited_without_claiming_memory_is_configured(self):
        report = learning_cycle_audit.audit_learning_cycle()
        self.assertEqual(report["status"], "ok")
        self.assertTrue(report["read_only"])
        self.assertTrue(report["ledger"]["valid"])
        self.assertEqual(report["skills"]["total"], 0)
        self.assertEqual(report["memory"]["status"], "disabled_missing_approval_key")
        self.assertIsNone(report["memory"]["rejected_or_unverifiable_records"])

    def test_missing_ledger_is_reported_without_creating_it(self):
        missing = self.root / "absent" / "ledger.sqlite3"
        with (
            patch.object(learning_cycle_audit, "DEFAULT_DB", missing),
            patch.dict(os.environ, {"CYBER_AI_LEDGER_PATH": str(missing)}),
        ):
            report = learning_cycle_audit.audit_learning_cycle()
        self.assertEqual(report["ledger"]["reason"], "database_missing")
        self.assertEqual(report["status"], "degraded")
        self.assertFalse(missing.exists())
        self.assertFalse(missing.parent.exists())

    def test_invalid_skill_review_window_is_rejected(self):
        for value in (0, -1, 3651, True, 1.5):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    learning_cycle_audit.audit_learning_cycle(
                        max_review_age_days=value
                    )

    def test_orphan_started_event_is_reported_but_not_reconciled(self):
        self.ledger.append(
            namespace="audit",
            task="test orphan",
            status="started",
            tool="test",
            evidence={"phase": "start"},
            duration_ms=0,
        )
        report = learning_cycle_audit.audit_learning_cycle()
        self.assertEqual(report["status"], "degraded")
        self.assertEqual(len(report["ledger"]["orphaned_started_events"]), 1)
        self.assertEqual(
            len(self.ledger.history(namespace="audit", limit=10)), 1
        )

    def test_invalid_skill_history_is_reported(self):
        skill = skillbook._insert_verified_skill(
            name="Skill de auditoría",
            task_pattern="auditoria defensiva",
            description="Prueba",
            prerequisites=[],
            methodology=["preparar fixture", "verificar resultado"],
            validation=["comparar salida"],
            tools=[],
            tags=["audit"],
            evidence=["fixture 1", "fixture 2"],
            source_urls=[],
            success_runs=2,
            failure_runs=0,
            verified_by="VERITAS",
            verifier_verdict="CONFIRMADA",
        )
        with skillbook.connect() as db:
            db.execute(
                "UPDATE skills SET description=? WHERE skill_id=?",
                ("Descripción manipulada", skill["skill_id"]),
            )
        report = learning_cycle_audit.audit_learning_cycle()
        self.assertEqual(report["status"], "degraded")
        self.assertEqual(
            report["skills"]["invalid_histories"][0]["reason"],
            "current_snapshot_mismatch",
        )

    def test_corrupted_ledger_is_reported_without_mutation(self):
        self.ledger.append(
            namespace="audit", task="integrity", status="completed",
            tool="test", evidence={"ok": True}, duration_ms=1,
        )
        with sqlite3.connect(self.ledger.path) as db:
            db.execute("DROP TRIGGER execution_events_no_update")
            db.execute("UPDATE execution_events SET task='tampered'")
        report = learning_cycle_audit.audit_learning_cycle()
        self.assertEqual(report["status"], "degraded")
        self.assertFalse(report["ledger"]["valid"])
        self.assertEqual(report["ledger"]["reason"], "event_hash")

    def test_report_write_is_atomic_and_private(self):
        destination = self.root / "reports" / "audit.json"
        report = {"status": "ok", "read_only": True}
        result = learning_cycle_audit.write_report(report, destination)
        self.assertEqual(result, destination)
        self.assertEqual(json.loads(destination.read_text()), report)
        if os.name == "posix":
            self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
        self.assertFalse(destination.with_name("audit.json.tmp").exists())

    def test_report_writer_rejects_symlink_destination(self):
        target = self.root / "target.json"
        target.write_text("{}", encoding="utf-8")
        link = self.root / "linked.json"
        link.symlink_to(target)
        with self.assertRaisesRegex(OSError, "enlaces simbólicos"):
            learning_cycle_audit.write_report({"status": "ok"}, link)


if __name__ == "__main__":
    unittest.main()
