import json
import unittest
from pathlib import Path
from knowledge_quality import audit_library

class KnowledgeQualityTests(unittest.TestCase):
    def test_curriculum_covers_manifest(self):
        report=audit_library()
        self.assertEqual(report["area_count"],48)
        self.assertEqual(report["curriculum_defined"],48)
        self.assertEqual(report["errors"],[])
    def test_each_domain_has_specific_topics_and_artifacts(self):
        root=Path(__file__).resolve().parents[1]
        data=json.loads((root/"knowledge/curricula/domain_curriculum.json").read_text(encoding="utf-8"))
        for area in data["areas"]:
            with self.subTest(area=area["id"]):
                self.assertGreaterEqual(len(area["deep_topics"]),5)
                self.assertGreaterEqual(len(area["required_artifacts"]),6)
                self.assertIn("L4",area["learning_levels"])
                self.assertTrue(area["lab_blueprint"]["scenarios"])
                self.assertTrue(area["evaluation"]["pass_rule"])
    def test_all_48_fundamental_packs_pass_structural_gate(self):
        report=audit_library()
        self.assertEqual(report["base_complete"],48, report["areas"])
        self.assertEqual(report["area_count"],48)

    def test_all_48_domains_have_substantive_deep_sections(self):
        report=audit_library()
        self.assertEqual(report["deep_complete"],48, report["areas"])
        self.assertEqual(report["deep_section_checks"],240)
        self.assertEqual(report["deep_content_checks"],240)
        for area in report["areas"]:
            with self.subTest(area=area["id"]):
                self.assertEqual(area["missing_deep_sections"],[])
                self.assertTrue(all(words >= 20 for words in area["deep_section_words"].values()))
    def test_curriculum_disclaims_expert_validation(self):
        root=Path(__file__).resolve().parents[1]
        data=json.loads((root/"knowledge/curricula/domain_curriculum.json").read_text(encoding="utf-8"))
        self.assertIn("no declara",data["disclaimer"])

    def test_all_manifest_domains_have_research_studies_with_references(self):
        report = audit_library()
        self.assertEqual(report["research_studies_complete"], 48)
        self.assertGreater(report["research_study_words_total"], 12000)
        self.assertGreater(report["research_study_references_total"], 100)
        for area in report["areas"]:
            with self.subTest(area=area["id"]):
                self.assertTrue(area["research_study_present"])
                self.assertGreaterEqual(area["research_study_words"], 250)
                self.assertGreaterEqual(area["research_study_references"], 2)


    def test_all_192_advanced_gaps_have_substantive_development(self):
        root = Path(__file__).resolve().parents[1]
        register = json.loads((root / "knowledge/research/ADVANCED_GAP_REGISTER.json").read_text(encoding="utf-8"))
        manifest = json.loads((root / "knowledge/packs/manifest.json").read_text(encoding="utf-8"))
        doc = (root / "knowledge/research/ADVANCED_GAP_DEVELOPMENT.md").read_text(encoding="utf-8")
        expected = {area["id"] for area in manifest["areas"]}
        self.assertEqual({area["domain_id"] for area in register["domains"]}, expected)
        self.assertEqual(len(register["domains"]), 48)
        total = 0
        for area in register["domains"]:
            with self.subTest(domain=area["domain_id"]):
                self.assertEqual(area["status"], "developed_initial_draft")
                self.assertEqual(len(area["developed_topics"]), 4)
                for item in area["developed_topics"]:
                    self.assertEqual(item["status"], "developed_initial_draft")
                    self.assertGreaterEqual(item["word_count"], 130)
                    self.assertIn(item["topic"], doc)
                    self.assertIn("### Laboratorio y evaluación", doc)
                    self.assertIn("### Evidencia y limitaciones", doc)
                    total += 1
        self.assertEqual(total, 192)

if __name__ == "__main__": unittest.main()
