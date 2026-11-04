"""Pruebas permanentes del modo de ejecución de CYBER_AI."""

import tempfile
import unittest
from pathlib import Path

import agent_runner as runner
import evidence_graph as graph


class TestExecutionMode(unittest.TestCase):
    def test_standard_mode_preserves_original_prompt(self):
        prompt = "Revisar permisos de Linux"

        result = runner.build_execution_prompt(prompt, "standard")

        self.assertEqual(result, prompt)

    def test_technical_mode_adds_technical_guidance(self):
        prompt = "Revisar permisos de Linux"

        result = runner.build_execution_prompt(prompt, "technical")

        self.assertIn("MODO DE EJECUCIÓN: TÉCNICO", result)
        self.assertIn(prompt, result)
        self.assertIn("No inventes resultados", result)

    def test_invalid_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            runner.build_execution_prompt(
                "Prueba", "modo_inexistente"
            )

    def test_checkpoint_preserves_mode_when_updated(self):
        original_db_path = graph.DB_PATH

        try:
            with tempfile.TemporaryDirectory() as temp:
                graph.DB_PATH = Path(temp) / "graph.sqlite3"

                graph.save_checkpoint(
                    task_id="technical-mode-test",
                    agent="TEST",
                    status="incomplete",
                    original_task="Revisar permisos de Linux",
                    mode="technical",
                    current_step="Comprobación 1",
                )

                checkpoint = graph.get_checkpoint(
                    "technical-mode-test"
                )
                self.assertEqual(checkpoint["mode"], "technical")

                # Actualizar el checkpoint sin indicar otro modo.
                graph.save_checkpoint(
                    task_id="technical-mode-test",
                    agent="TEST",
                    status="incomplete",
                    current_step="Comprobación 2",
                )

                checkpoint = graph.get_checkpoint(
                    "technical-mode-test"
                )
                self.assertEqual(checkpoint["mode"], "technical")

        finally:
            graph.DB_PATH = original_db_path


if __name__ == "__main__":
    unittest.main()
