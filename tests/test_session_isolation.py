"""Comprueba que el grafo no mezcla el contexto entre sesiones."""

import tempfile
import unittest
from pathlib import Path

import evidence_graph as graph


class TestSessionIsolation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_db = graph.DB_PATH
        graph.DB_PATH = Path(self.temp.name) / "sessions.sqlite3"

    def tearDown(self):
        graph.DB_PATH = self.original_db
        self.temp.cleanup()

    def test_context_only_contains_its_session(self):
        linux = graph.create_session("Auditoría Linux")
        ollama = graph.create_session("Investigación Ollama")

        graph.add_node(
            session_id=linux,
            task_id="linux-task",
            kind="fact",
            content="DATO PRIVADO DE LINUX",
        )
        graph.add_node(
            session_id=ollama,
            task_id="ollama-task",
            kind="fact",
            content="DATO PRIVADO DE OLLAMA",
        )

        linux_context = graph.build_context(session_id=linux)
        ollama_context = graph.build_context(session_id=ollama)

        self.assertIn("DATO PRIVADO DE LINUX", linux_context)
        self.assertNotIn("DATO PRIVADO DE OLLAMA", linux_context)
        self.assertIn("DATO PRIVADO DE OLLAMA", ollama_context)
        self.assertNotIn("DATO PRIVADO DE LINUX", ollama_context)

    def test_focus_node_from_another_session_is_excluded(self):
        linux = graph.create_session("Linux")
        ollama = graph.create_session("Ollama")

        foreign_node = graph.add_node(
            session_id=ollama,
            kind="fact",
            content="NO DEBE APARECER",
        )

        context = graph.build_context(
            session_id=linux,
            focus_node_ids=[foreign_node],
        )
        self.assertNotIn("NO DEBE APARECER", context)

    def test_unknown_session_is_rejected(self):
        with self.assertRaises(ValueError):
            graph.build_context(session_id="sesion-que-no-existe")


if __name__ == "__main__":
    unittest.main()
