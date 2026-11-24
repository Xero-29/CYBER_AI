"""Regression checks for domain-specific Foundations and AI Red Team material.

These tests validate navigation and prevent known generic-placeholder regressions.
They do not assess technical truth, expert competence, source support, or lab execution.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DomainSpecificKnowledgeTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_ai_red_team_compendium_does_not_repeat_generic_topic_boilerplate(self):
        text = self.read("knowledge/deep_modules/ai_red_team/TECHNICAL_COMPENDIUM.md")
        self.assertIn("AI_RED_TEAM_THEORETICAL_DEVELOPMENT_V1.md", text)
        self.assertIn("AI_RED_TEAM_TEST_CATALOG_V1.md", text)
        self.assertNotIn("Fundamentos y modelo:** explicar arquitectura, componentes", text)
        self.assertIn("siete líneas de trabajo", text.lower())

    def test_ai_red_team_catalog_defines_nine_distinct_test_cases(self):
        text = self.read("knowledge/deep_modules/ai_red_team/AI_RED_TEAM_TEST_CATALOG_V1.md")
        ids = re.findall(r"^### (ART-\d{2}) —", text, re.MULTILINE)
        self.assertEqual(ids, [f"ART-{number:02d}" for number in range(1, 10)])
        self.assertIn("cross_tenant_leakage_rate", text)
        self.assertIn("unauthorized_action_rate", text)
        self.assertIn("INCONCLUSIVE", text)
        self.assertIn("NOT RUN", text)

    def test_ai_red_team_readme_topics_are_specific_not_generic_placeholders(self):
        text = self.read("knowledge/deep_modules/ai_red_team/README.md")
        self.assertIn("procedencia e integridad", text)
        self.assertIn("aislamiento entre tenants", text)
        self.assertNotIn("Investigar arquitectura y dependencias; conceptos y variantes", text)

    def test_foundations_risk_engineering_has_explicit_models_and_limits(self):
        text = self.read("knowledge/deep_modules/foundations/FOUNDATIONS_RISK_ENGINEERING_V1.md")
        for marker in (
            "E[L]", "ALE", "Incertidumbre", "CVSS", "Ejemplo resuelto",
            "Evidencia", "lectura integral", "laboratorio",
        ):
            self.assertIn(marker.lower(), text.lower())
        self.assertIn("no se declara ejecutado", text.lower())

    def test_foundations_readme_routes_to_specific_risk_material(self):
        text = self.read("knowledge/deep_modules/foundations/README.md")
        self.assertIn("FOUNDATIONS_RISK_ENGINEERING_V1.md", text)
        self.assertNotIn("dominar este componente dentro del alcance de Fundamentos", text)


if __name__ == "__main__":
    unittest.main()
