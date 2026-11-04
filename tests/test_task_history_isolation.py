"""Verifica que las tareas aisladas no reciban historiales ajenos."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner as runner


class TestTaskHistoryIsolation(unittest.TestCase):
    def test_excludes_records_with_another_task_id(self):
        original_log = runner.TASK_LOG

        try:
            with tempfile.TemporaryDirectory() as temp:
                runner.TASK_LOG = Path(temp) / "tasks.jsonl"

                records = [
                    {
                        "task_id": "other-task",
                        "agent": "FILTRO",
                        "task": "TAREA AJENA: investigar autenticación de Ollama",
                        "response": "RESPUESTA AJENA: información de Ollama",
                    },
                    {
                        "task_id": "target-task",
                        "agent": "FARO",
                        "task": "TAREA PROPIA: auditar seguridad Linux",
                        "response": "RESPUESTA PROPIA: revisar permisos",
                    },
                ]

                runner.TASK_LOG.write_text(
                    "".join(
                        json.dumps(item, ensure_ascii=False) + "\n"
                        for item in records
                    ),
                    encoding="utf-8",
                )

                agent = {
                    "memory": {},
                    "context": {
                        "enabled": True,
                        "sources": ["recent_agent_tasks"],
                        "max_items": 10,
                        "max_chars_per_field": 500,
                        "include_task": True,
                        "include_response": True,
                    },
                }

                with (
                    patch.object(
                        runner, "build_evidence_context", return_value=""
                    ),
                    patch.object(runner, "get_checkpoint", return_value=None),
                ):
                    result = runner.build_task_prompt(
                        agent,
                        "Continúa la auditoría de Linux.",
                        task_id="target-task",
                        isolate_history=True,
                    )

                self.assertIn("TAREA PROPIA: auditar seguridad Linux", result)
                self.assertNotIn("TAREA AJENA: investigar autenticación", result)
                self.assertNotIn("RESPUESTA AJENA: información de Ollama", result)

        finally:
            runner.TASK_LOG = original_log


if __name__ == "__main__":
    unittest.main()
