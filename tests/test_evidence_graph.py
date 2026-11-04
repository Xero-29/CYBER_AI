"""Pruebas básicas del grafo de evidencia."""

import tempfile
import unittest
from pathlib import Path

import evidence_graph as graph


class TestEvidenceGraph(unittest.TestCase):
    def setUp(self):
        self.original_db = graph.DB_PATH
        self.temp_dir = tempfile.TemporaryDirectory()
        graph.DB_PATH = Path(self.temp_dir.name) / "test.sqlite3"
        graph.initialize()

    def tearDown(self):
        graph.DB_PATH = self.original_db
        self.temp_dir.cleanup()

    def test_nodes_relations_and_checkpoint(self):
        source = graph.add_node(
            task_id="t1",
            kind="source",
            content="Documentación de prueba",
            status="reviewed",
            source_url="https://docs.ollama.com/api/usage",
            source_quote="Evidencia de prueba.",
        )
        claim = graph.add_node(
            task_id="t1",
            kind="claim",
            content="Afirmación de prueba",
            status="pending",
        )
        graph.add_edge(claim, "supported_by", source)
        graph.save_checkpoint(
            task_id="t1",
            agent="VERITAS",
            status="incomplete",
            next_action="Verificar la afirmación",
            focus_node_ids=[claim, source],
        )

        checkpoint = graph.get_checkpoint("t1")
        self.assertEqual(checkpoint["status"], "incomplete")
        self.assertEqual(checkpoint["next_action"], "Verificar la afirmación")

        context = graph.build_context(
            task_id="t1",
            focus_node_ids=checkpoint["focus_node_ids"],
        )
        self.assertIn("Afirmación de prueba", context)
        self.assertIn("https://docs.ollama.com/api/usage", context)
        self.assertIn("supported_by", context)

    def test_context_requires_a_target(self):
        with self.assertRaises(ValueError):
            graph.build_context()

    def test_invalid_confidence_is_rejected(self):
        with self.assertRaises(ValueError):
            graph.add_node(
                kind="claim",
                content="Prueba",
                confidence=1.5,
            )


if __name__ == "__main__":
    unittest.main()
