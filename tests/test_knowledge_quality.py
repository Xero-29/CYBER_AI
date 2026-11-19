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
    def test_audit_does_not_claim_shallow_packs_are_deep(self):
        report=audit_library()
        self.assertLess(report["deep_complete"],report["area_count"])
        self.assertGreater(report["deep_section_checks"],0)
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

if __name__ == "__main__": unittest.main()
