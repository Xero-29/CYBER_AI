"""Pruebas de seguridad y aislamiento de la memoria compartida."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import learning_memory
import agent_runner


class LearningMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_path = Path(self.temp_dir.name) / "lessons.jsonl"
        self.memory_patch = patch.object(
            learning_memory, "MEMORY_FILE", self.memory_path
        )
        self.memory_patch.start()

    def tearDown(self):
        self.memory_patch.stop()
        self.temp_dir.cleanup()

    def save_lesson(self, namespaces=None):
        return learning_memory.save_verified_lesson(
            topic="Autenticacion local Ollama",
            error="Confundir la API local con la API en la nube",
            correction=(
                "La API local no requiere autenticacion; "
                "la API en la nube requiere una clave."
            ),
            evidence=[
                "La documentacion oficial distingue el acceso local "
                "del acceso a los servicios en la nube."
            ],
            source_urls=[
                "https://docs.ollama.com/api/authentication"
            ],
            tags=["ollama", "api", "autenticacion"],
            namespaces=namespaces or ["nexo", "forja"],
            verified_by="VERITAS",
            verifier_verdict="RESPALDADA",
        )

    def test_solo_lee_lecciones_verificadas(self):
        self.save_lesson()

        # Simular una propuesta pendiente de verificacion.
        pending = {
            "status": "pending",
            "verified_by": "FILTRO",
            "verifier_verdict": "PENDIENTE",
            "topic": "Leccion pendiente",
            "error": "Error candidato",
            "correction": "Correccion no confirmada",
            "evidence": ["Evidencia pendiente"],
            "source_urls": ["https://example.org"],
            "namespaces": ["nexo"],
        }
        with self.memory_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(pending) + "\n")

        lessons = learning_memory.read_lessons()
        self.assertEqual(len(lessons), 1)
        self.assertEqual(lessons[0]["verified_by"], "VERITAS")

    def test_rechaza_aprobacion_no_confirmada(self):
        with self.assertRaises(ValueError):
            learning_memory.save_verified_lesson(
                topic="Prueba",
                error="Error",
                correction="Correccion",
                evidence=["Texto de evidencia"],
                source_urls=["https://docs.ollama.com"],
                tags=["prueba"],
                namespaces=["nexo"],
                verified_by="FILTRO",
                verifier_verdict="PARCIAL",
            )

    def test_limita_la_leccion_a_sus_agentes(self):
        self.save_lesson()

        nexo_context = learning_memory.build_memory_context(
            "Autenticacion local Ollama",
            namespace="nexo",
        )
        veritas_context = learning_memory.build_memory_context(
            "Autenticacion local Ollama",
            namespace="veritas",
        )

        self.assertIn("Correccion verificada", nexo_context)
        self.assertEqual(veritas_context, "")

    def test_ejecutor_inyecta_lecciones_en_la_tarea(self):
        expected = "LECCION DE PRUEBA VERIFICADA"

        with patch.object(
            agent_runner,
            "build_memory_context",
            return_value=expected,
        ):
            result = agent_runner.build_task_prompt(
                {"memory": {"namespace": "nexo"}},
                "Investigar autenticacion local de Ollama",
            )

        self.assertIn(expected, result)
        self.assertIn("Investigar autenticacion local", result)


if __name__ == "__main__":
    unittest.main()
