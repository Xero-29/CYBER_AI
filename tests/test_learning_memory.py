"""Pruebas de firma, procedencia y aislamiento de la memoria compartida."""

import hashlib
import hmac
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_runner
import learning_memory


class FakeLedger:
    def __init__(self, events, valid=True):
        self.events = events
        self.valid = valid

    def verify(self):
        return {"valid": self.valid}

    def history(self, **kwargs):
        return self.events


class LearningMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_path = Path(self.temp_dir.name) / "lessons.jsonl"
        self.memory_patch = patch.object(
            learning_memory, "MEMORY_FILE", self.memory_path
        )
        self.memory_patch.start()
        self.key = "test-veritas-approval-key-with-at-least-32-bytes"
        self.key_patch = patch.dict(
            os.environ, {learning_memory.APPROVAL_KEY_ENV: self.key}
        )
        self.key_patch.start()
        self.events = [
            {
                "event_id": "memory-run-1",
                "task_fingerprint": "a" * 64,
                "status": "completed",
                "created_at": "2026-01-01T00:00:00Z",
                "validator_results": [{"passed": True}],
                "evidence_sha256": "1" * 64,
            },
            {
                "event_id": "memory-run-2",
                "task_fingerprint": "a" * 64,
                "status": "completed",
                "created_at": "2026-01-02T00:00:00Z",
                "validator_results": [{"passed": True}],
                "evidence_sha256": "2" * 64,
            },
        ]
        self.args = {
            "topic": "Autenticacion local Ollama",
            "error": "Confundir la API local con la API en la nube",
            "correction": (
                "La API local no requiere autenticacion; "
                "la API en la nube requiere una clave."
            ),
            "evidence": [
                "La documentacion oficial distingue el acceso local "
                "del acceso a los servicios en la nube."
            ],
            "source_urls": ["https://docs.ollama.com/api/authentication"],
            "tags": ["ollama", "api", "autenticacion"],
            "namespaces": ["nexo", "forja"],
            "namespace": "nexo",
            "event_ids": ["memory-run-1", "memory-run-2"],
        }

    def tearDown(self):
        self.key_patch.stop()
        self.memory_patch.stop()
        self.temp_dir.cleanup()

    def save_lesson(self, **overrides):
        args = dict(self.args)
        args.update(overrides)
        ledger = FakeLedger(self.events)
        with patch.object(learning_memory, "ExecutionLedger", return_value=ledger):
            payload = learning_memory.build_lesson_approval_payload(**args)
            signature = hmac.new(
                self.key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            return learning_memory.save_verified_lesson_from_ledger(
                **args, approval_signature=signature
            )

    def test_only_signed_ledger_backed_lessons_are_read(self):
        self.save_lesson()
        pending = {
            "schema_version": 1,
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
        self.assertEqual(lessons[0]["schema_version"], 2)

    def test_without_approval_key_memory_fails_closed(self):
        self.save_lesson()
        with patch.dict(os.environ, {learning_memory.APPROVAL_KEY_ENV: ""}):
            self.assertEqual(learning_memory.read_lessons(), [])

    def test_direct_self_asserted_registration_is_disabled(self):
        with self.assertRaisesRegex(ValueError, "Registro directo deshabilitado"):
            learning_memory.save_verified_lesson(
                verified_by="VERITAS", verifier_verdict="CONFIRMADA"
            )

    def test_invalid_signature_is_rejected(self):
        with patch.object(
            learning_memory, "ExecutionLedger",
            return_value=FakeLedger(self.events),
        ):
            with self.assertRaisesRegex(ValueError, "Firma VERITAS inválida"):
                learning_memory.save_verified_lesson_from_ledger(
                    **self.args, approval_signature="0" * 64
                )

    def test_failed_ledger_event_blocks_memory_promotion(self):
        events = self.events + [{
            "event_id": "memory-run-3",
            "task_fingerprint": "a" * 64,
            "status": "failed",
            "created_at": "2026-01-03T00:00:00Z",
            "validator_results": [{"passed": False}],
            "evidence_sha256": "3" * 64,
        }]
        args = dict(self.args, event_ids=["memory-run-1", "memory-run-2"])
        with patch.object(
            learning_memory, "ExecutionLedger", return_value=FakeLedger(events)
        ):
            with self.assertRaisesRegex(ValueError, "fallidas"):
                learning_memory.build_lesson_approval_payload(**args)

    def test_corrupted_signed_record_is_not_taught(self):
        self.save_lesson()
        record = json.loads(self.memory_path.read_text(encoding="utf-8"))
        record["correction"] = "Una correccion manipulada"
        self.memory_path.write_text(
            json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        self.assertEqual(learning_memory.read_lessons(), [])

    def test_duplicate_lesson_is_not_written_twice(self):
        first = self.save_lesson()
        second = self.save_lesson()
        self.assertTrue(first["saved"])
        self.assertFalse(second["saved"])
        self.assertEqual(len(learning_memory.read_lessons()), 1)

    def test_lesson_is_limited_to_its_agents(self):
        self.save_lesson()
        nexo_context = learning_memory.build_memory_context(
            "Autenticacion local Ollama", namespace="nexo"
        )
        veritas_context = learning_memory.build_memory_context(
            "Autenticacion local Ollama", namespace="veritas"
        )
        self.assertIn("Corrección verificada", nexo_context)
        self.assertEqual(veritas_context, "")

    def test_executor_injects_signed_lessons_into_task(self):
        expected = "LECCION DE PRUEBA VERIFICADA"
        with patch.object(
            agent_runner, "build_memory_context", return_value=expected
        ):
            result = agent_runner.build_task_prompt(
                {"memory": {"namespace": "nexo"}},
                "Investigar autenticacion local de Ollama",
            )
        self.assertIn(expected, result)
        self.assertIn("Investigar autenticacion local", result)


if __name__ == "__main__":
    unittest.main()
