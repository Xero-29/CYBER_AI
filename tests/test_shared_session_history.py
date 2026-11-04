"""Prueba que los agentes compartan historial solo dentro de su sesión."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner as runner


class TestSharedSessionHistory(unittest.TestCase):
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
        finally:
            runner.TASK_LOG = previous_log


if __name__ == "__main__":
    unittest.main()
