"""Prueba la continuación automática y el almacenamiento comprimido."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner as runner
import evidence_graph as graph
import compressed_store
import compressed_checkpoint


class TestAutomaticContinuation(unittest.TestCase):
    def test_stops_and_preserves_checkpoint_when_paragraph_repeats(self):
        original_paths = (
            graph.DB_PATH,
            runner.LOCK_FILE,
            runner.TASK_LOG,
            compressed_store.DB_PATH,
        )

        try:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                graph.DB_PATH = root / "graph.sqlite3"
                runner.LOCK_FILE = root / "runner.lock"
                runner.TASK_LOG = root / "tasks.jsonl"
                compressed_store.DB_PATH = root / "compressed.sqlite3"

                agent = {
                    "model": "test-model",
                    "parameters": {},
                    "memory": {},
                    "context": {"enabled": False},
                    "instructions": "Agente simulado de pruebas.",
                }

                paragraph = (
                    "Esta comprobación defensiva revisa los permisos "
                    "configurados y los contrasta con la política "
                    "documentada para identificar posibles anomalías. "
                    * 12
                ).strip()

                responses = [
                    {
                        "message": {"content": paragraph, "thinking": ""},
                        "done_reason": "length",
                        "prompt_eval_count": 100,
                        "eval_count": 100,
                    },
                    {
                        "message": {"content": paragraph, "thinking": ""},
                        "done_reason": "stop",
                        "prompt_eval_count": 20,
                        "eval_count": 50,
                    },
                ]
                requests = []

                def fake_response(endpoint, payload=None, timeout=600, provider=None):
                    self.assertEqual(endpoint, "api/chat")
                    requests.append(payload)
                    if not responses:
                        self.fail("Se solicitó un fragmento inesperado.")
                    return responses.pop(0)

                with (
                    patch.object(
                        runner, "load_config",
                        return_value={"resource_policy": {}},
                    ),
                    patch.object(
                        runner, "resolve_agent",
                        return_value=("TEST", agent),
                    ),
                    patch.object(
                        runner,
                        "resolve_provider",
                        return_value={
                            "name": "test",
                            "protocol": "ollama",
                            "base_url": "http://127.0.0.1:11434",
                        },
                    ),
                    patch.object(
                        runner, "provider_models", return_value={"test-model"}
                    ),
                    patch.object(
                        runner, "installed_models",
                        return_value={"test-model"},
                    ),
                    patch.object(runner, "unload_other_models"),
                    patch.object(
                        runner, "request_json", side_effect=fake_response
                    ),
                    patch.object(runner, "record"),
                    patch.object(
                        runner, "build_memory_context", return_value=""
                    ),
                    patch("builtins.print"),
                ):
                    runner.run_agent(
                        "TEST",
                        "Genera una respuesta de prueba.",
                        num_predict_override=100,
                        task_id="repeated-paragraph-test",
                    )

                self.assertEqual(len(requests), 2)

                checkpoint = graph.get_checkpoint("repeated-paragraph-test")
                self.assertIsNotNone(checkpoint)
                self.assertEqual(checkpoint["status"], "incomplete")
                self.assertIn("repetido", checkpoint["next_action"])

                assembled = compressed_checkpoint.restore_partial_output(
                    checkpoint["partial_output"],
                    checkpoint["session_id"],
                )
                self.assertEqual(assembled, paragraph)

                events = [
                    json.loads(line)
                    for line in runner.TASK_LOG.read_text(
                        encoding="utf-8"
                    ).splitlines()
                    if line.strip()
                ]
                event = events[-1]
                self.assertTrue(event["repetition_detected"])
                self.assertEqual(
                    event["rejected_repeated_fragment"], paragraph
                )
                self.assertEqual(event["response"], paragraph)

        finally:
            (
                graph.DB_PATH,
                runner.LOCK_FILE,
                runner.TASK_LOG,
                compressed_store.DB_PATH,
            ) = original_paths


    def test_assembles_three_fragments_without_losing_text(self):
        # Guardar las rutas originales para aislar completamente la prueba.
        original_paths = (
            graph.DB_PATH,
            runner.LOCK_FILE,
            runner.TASK_LOG,
            compressed_store.DB_PATH,
        )

        try:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)

                graph.DB_PATH = root / "graph.sqlite3"
                runner.LOCK_FILE = root / "runner.lock"
                runner.TASK_LOG = root / "tasks.jsonl"
                compressed_store.DB_PATH = root / "compressed.sqlite3"

                agent = {
                    "model": "test-model",
                    "parameters": {},
                    "memory": {},
                    "context": {"enabled": False},
                    "instructions": "Agente simulado de pruebas.",
                }

                # Simular una respuesta extensa sin llamar a Ollama.
                first_text = (
                    "INICIO DE RESPUESTA " + ("x" * 8000)
                    + "\nFINAL DEL PRIMER FRAGMENTO"
                )
                second_text = "\nSEGUNDO FRAGMENTO"
                third_text = "\nTERCER FRAGMENTO COMPLETO"

                responses = [
                    {
                        "message": {"content": first_text, "thinking": ""},
                        "done_reason": "length",
                        "prompt_eval_count": 100,
                        "prompt_eval_cached_count": 10,
                        "eval_count": 101,
                        "total_duration": 1000,
                    },
                    {
                        "message": {"content": second_text, "thinking": ""},
                        "done_reason": "length",
                        "prompt_eval_count": 20,
                        "prompt_eval_cached_count": 5,
                        "eval_count": 40,
                        "total_duration": 2000,
                    },
                    {
                        "message": {"content": third_text, "thinking": ""},
                        "done_reason": "stop",
                        "prompt_eval_count": 30,
                        "prompt_eval_cached_count": 5,
                        "eval_count": 50,
                        "total_duration": 3000,
                    },
                ]

                requests = []

                def fake_response(endpoint, payload=None, timeout=600, provider=None):
                    self.assertEqual(endpoint, "api/chat")
                    requests.append(payload)
                    if not responses:
                        self.fail("Se solicitaron más fragmentos de los esperados.")
                    return responses.pop(0)

                with (
                    patch.object(
                        runner,
                        "load_config",
                        return_value={"resource_policy": {}},
                    ),
                    patch.object(
                        runner,
                        "resolve_agent",
                        return_value=("TEST", agent),
                    ),
                    patch.object(
                        runner,
                        "resolve_provider",
                        return_value={
                            "name": "test",
                            "protocol": "ollama",
                            "base_url": "http://127.0.0.1:11434",
                        },
                    ),
                    patch.object(
                        runner, "provider_models", return_value={"test-model"}
                    ),
                    patch.object(
                        runner,
                        "installed_models",
                        return_value={"test-model"},
                    ),
                    patch.object(runner, "unload_other_models"),
                    patch.object(
                        runner, "request_json", side_effect=fake_response
                    ),
                    patch.object(runner, "record"),
                    patch.object(
                        runner, "build_memory_context", return_value=""
                    ),
                    patch("builtins.print"),
                ):
                    # Una sola llamada debe consumir los tres fragmentos.
                    runner.run_agent(
                        "TEST",
                        "Genera el informe de prueba.",
                        num_predict_override=100,
                        task_id="auto-continue-test",
                    )

                self.assertEqual(len(requests), 3)

                checkpoint = graph.get_checkpoint("auto-continue-test")
                self.assertIsNotNone(checkpoint)
                self.assertEqual(
                    checkpoint["status"], "generation_finished"
                )

                assembled = compressed_checkpoint.restore_partial_output(
                    checkpoint["partial_output"],
                    checkpoint["session_id"],
                )

                expected = first_text + second_text + third_text
                self.assertEqual(assembled, expected)
                self.assertGreater(len(assembled), 8000)

                # La tercera petición debe conservar el protocolo de continuación.
                self.assertEqual(
                    requests[1]["messages"][0]["role"], "system"
                )
                self.assertEqual(
                    requests[2]["messages"][0]["role"], "system"
                )

                # Comprobar que el registro suma métricas de las tres peticiones.
                events = [
                    json.loads(line)
                    for line in runner.TASK_LOG.read_text(
                        encoding="utf-8"
                    ).splitlines()
                    if line.strip()
                ]
                event = events[-1]

                self.assertEqual(event["generation_requests"], 3)
                self.assertEqual(event["continuations"], 2)
                self.assertEqual(event["eval_count"], 191)
                self.assertEqual(event["prompt_eval_count"], 150)
                self.assertEqual(event["total_duration_ns"], 6000)
                self.assertEqual(event["response"], expected)

        finally:
            (
                graph.DB_PATH,
                runner.LOCK_FILE,
                runner.TASK_LOG,
                compressed_store.DB_PATH,
            ) = original_paths


if __name__ == "__main__":
    unittest.main()
