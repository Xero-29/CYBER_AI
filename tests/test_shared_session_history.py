import hashlib
"""Prueba que los agentes compartan historial solo dentro de su sesión."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner as runner


class TestSharedSessionHistory(unittest.TestCase):
    def test_new_history_uses_hashed_session_id_and_keeps_isolation(self):
        previous_log = runner.TASK_LOG
        try:
            with tempfile.TemporaryDirectory() as temp:
                runner.TASK_LOG = Path(temp) / "tasks.jsonl"
                session_id = "session-privacy-test"
                runner.save_jsonl(runner.TASK_LOG, {
                    "task_id": "task-nexo",
                    "session_id": session_id,
                    "agent": "NEXO",
                    "task": "Revisar password=private-task-secret",
                    "response": "Hallazgo token=private-response-secret",
                })
                stored = json.loads(runner.TASK_LOG.read_text(encoding="utf-8"))
                self.assertEqual(stored["session_id"], "[REDACTED]")
                self.assertEqual(
                    stored["session_fingerprint"],
                    hashlib.sha256(session_id.encode("utf-8")).hexdigest(),
                )
                prompt = runner.build_task_prompt(
                    {"context": {"enabled": False}},
                    "tarea actual",
                    task_id="task-filtro",
                    session_id=session_id,
                    isolate_history=True,
                    context_task_ids=["task-nexo"],
                )
                self.assertIn("NEXO", prompt)
                self.assertIn("password=[REDACTED]", prompt)
                self.assertIn("token=[REDACTED]", prompt)
                self.assertNotIn("private-task-secret", prompt)
                self.assertNotIn("private-response-secret", prompt)
        finally:
            runner.TASK_LOG = previous_log


    def test_agent_without_legacy_context_reads_own_session(self):
        previous_log = runner.TASK_LOG

        try:
            with tempfile.TemporaryDirectory() as temp:
                runner.TASK_LOG = Path(temp) / "tasks.jsonl"

                records = [
                    {
                        "task_id": "task-nexo",
                        "session_id": "linux-session",
                        "agent": "NEXO",
                        "task": "Investigar permisos de Linux.",
                        "response": "NEXO recomienda revisar permisos con stat.",
                    },
                    {
                        "task_id": "task-other",
                        "session_id": "ollama-session",
                        "agent": "FILTRO",
                        "task": "Investigación ajena.",
                        "response": "DATO QUE NO DEBE APARECER.",
                    },
                ]

                runner.TASK_LOG.write_text(
                    "".join(json.dumps(x) + "\n" for x in records),
                    encoding="utf-8",
                )

                agent = {
                    "memory": {},
                    "context": {"enabled": False},
                }

                with (
                    patch.object(
                        runner, "build_evidence_context", return_value=""
                    ),
                    patch.object(
                        runner, "get_checkpoint", return_value=None
                    ),
                    patch.object(
                        runner, "build_memory_context", return_value=""
                    ),
                ):
                    prompt = runner.build_task_prompt(
                        agent,
                        "FILTRO debe revisar la investigación.",
                        task_id="task-filtro",
                        session_id="linux-session",
                        isolate_history=True,
                        context_task_ids=["task-nexo"],
                    )

                self.assertIn("NEXO recomienda revisar permisos", prompt)
                self.assertNotIn("DATO QUE NO DEBE APARECER", prompt)
                self.assertNotIn("legacy-task-secret", prompt)
                self.assertNotIn("legacy-response-secret", prompt)
                self.assertIn("password=[REDACTED]", prompt)
                self.assertIn("token=[REDACTED]", prompt)
        finally:
            runner.TASK_LOG = previous_log


if __name__ == "__main__":
    unittest.main()
