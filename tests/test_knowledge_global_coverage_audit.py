import unittest
from knowledge_global_coverage_audit import audit


class GlobalCoverageAuditTests(unittest.TestCase):
    def test_crosswalk_matches_all_manifest_areas(self):
        report = audit()
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(report["area_count"], 48)
        self.assertEqual(report["areas_with_reference_mapping"], 48)
        self.assertGreaterEqual(report["reference_count"], 40)
        self.assertEqual(report["cross_cutting_gap_count"], 8)
        self.assertFalse(report["exhaustive_coverage_claim"])
        self.assertEqual(report["content_depth_assessed"], 0)
        self.assertEqual(report["compendia_present"], 48)
        self.assertEqual(report["compendia_missing"], [])

    def test_every_area_reference_id_exists(self):
        report = audit()
        self.assertTrue(all(row["references_exist"] for row in report["areas"]))

    def test_reference_mapping_is_bidirectional(self):
        report = audit()
        self.assertTrue(report["ok"], report["errors"])

    def test_curriculum_topics_are_explicitly_accounted_for(self):
        report = audit()
        self.assertGreater(report["topic_requirement_count"], 300)
        self.assertEqual(report["topics_assessed"], 0)
        self.assertTrue(all(row["topic_count"] > 0 for row in report["areas"]))

    def test_required_artifacts_and_validation_gates_exist(self):
        report = audit()
        self.assertGreater(report["artifact_requirement_count"], 400)
        self.assertEqual(report["artifacts_assessed"], 0)
        self.assertEqual(report["validation_gate_count"], 48 * 7)
        self.assertEqual(report["validation_gates_assessed"], 0)

    def test_no_specialty_is_falsely_marked_validated(self):
        report = audit()
        self.assertEqual(report["validated_specialties"], 0)
        self.assertTrue(all(row["specialty_readiness"] == "requirements_defined_not_assessed"
                            for row in report["areas"]))

    def test_reference_mapping_does_not_imply_content_depth(self):
        report = audit()
        self.assertTrue(all(row["content_depth_status"] == "not_assessed_by_this_crosswalk"
                            for row in report["areas"]))


if __name__ == "__main__":
    unittest.main()
