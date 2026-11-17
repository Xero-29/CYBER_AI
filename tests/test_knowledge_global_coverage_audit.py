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

    def test_every_area_reference_id_exists(self):
        report = audit()
        self.assertTrue(all(row["references_exist"] for row in report["areas"]))

    def test_reference_mapping_does_not_imply_content_depth(self):
        report = audit()
        self.assertTrue(all(row["content_depth_status"] == "not_assessed_by_this_crosswalk"
                            for row in report["areas"]))


if __name__ == "__main__":
    unittest.main()
