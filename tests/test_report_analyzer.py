import unittest

from report_analyzer import analyze_report, analyze_scan


class ReportAnalyzerTests(unittest.TestCase):

    def test_detects_cve_reference(self):
        result = analyze_report("Hallazgo relacionado con CVE-2024-12345")
        self.assertEqual(result["cve_references"], ["CVE-2024-12345"])
        self.assertEqual(result["classification"], "known_reference")

    def test_no_cve_does_not_claim_novelty(self):
        result = analyze_report("Posible error de validación de entrada")
        self.assertEqual(result["classification"], "pending_validation")
        self.assertTrue(result["requires_manual_validation"])

    def test_patch_is_never_assumed(self):
        result = analyze_report("CVE-2023-12345")
        self.assertEqual(result["patch_status"], "unverified")
        self.assertFalse(result["confirmed_vulnerability"])

    def test_analyze_scan_groups_findings_and_counts_severity(self):
        data = {
            "target": "http://127.0.0.1:8765",
            "status": "completed",
            "findings": [
                {
                    "template-id": "test-header",
                    "matcher-name": "missing-header",
                    "matched-at": "http://127.0.0.1:8765",
                    "info": {"name": "Missing Header", "severity": "info"},
                },
                {
                    "template-id": "test-header",
                    "matcher-name": "missing-header",
                    "matched-at": "http://127.0.0.1:8765",
                    "info": {"name": "Missing Header", "severity": "info"},
                },
            ],
        }

        result = analyze_scan(data)

        self.assertEqual(result["raw_findings_count"], 2)
        self.assertEqual(result["grouped_findings_count"], 1)
        self.assertEqual(result["severity_counts"], {"info": 2})
        self.assertTrue(result["requires_manual_validation"])
        self.assertFalse(result["confirmed_vulnerability"])

    def test_unknown_finding_receives_generic_guidance(self):
        result = analyze_scan({
            "target": "http://127.0.0.1:8765",
            "status": "completed",
            "findings": [{
                "template-id": "unknown-template",
                "matcher-name": "unknown-matcher",
                "matched-at": "http://127.0.0.1:8765",
                "info": {"name": "Unknown Finding", "severity": "info"},
            }],
        })

        finding = result["findings"][0]
        self.assertTrue(finding["description"])
        self.assertTrue(finding["potential_risk"])
        self.assertTrue(finding["manual_validation"])
        self.assertTrue(finding["recommendation"])
        self.assertIn("no puede determinarse", finding["potential_risk"])

    def test_missing_security_headers_receives_specific_guidance(self):
        result = analyze_scan({
            "target": "http://127.0.0.1:8765",
            "status": "completed",
            "findings": [{
                "template-id": "http-missing-security-headers",
                "matcher-name": "permissions-policy",
                "matched-at": "http://127.0.0.1:8765",
                "info": {"name": "Missing Security Header", "severity": "info"},
            }],
        })

        finding = result["findings"][0]
        self.assertIn("permissions-policy", finding["description"].lower())
        self.assertTrue(finding["potential_risk"])
        self.assertTrue(finding["manual_validation"])
        self.assertIn("permissions-policy", finding["recommendation"].lower())



    def test_each_security_header_has_specific_guidance(self):
        headers = [
            "permissions-policy",
            "cross-origin-embedder-policy",
            "cross-origin-opener-policy",
            "cross-origin-resource-policy",
        ]

        recommendations = []

        for header in headers:
            with self.subTest(header=header):
                result = analyze_scan({
                    "target": "http://127.0.0.1:8765",
                    "status": "completed",
                    "findings": [{
                        "template-id": "http-missing-security-headers",
                        "matcher-name": header,
                        "matched-at": "http://127.0.0.1:8765",
                        "info": {
                            "name": "Missing Security Header",
                            "severity": "info",
                        },
                    }],
                })

                finding = result["findings"][0]
                self.assertTrue(finding["description"])
                self.assertTrue(finding["potential_risk"])
                self.assertTrue(finding["manual_validation"])
                self.assertTrue(finding["recommendation"])
                recommendations.append(finding["recommendation"])

        self.assertEqual(len(set(recommendations)), 4)

    def test_unknown_security_header_has_generic_guidance(self):
        result = analyze_scan({
            "target": "http://127.0.0.1:8765",
            "status": "completed",
            "findings": [{
                "template-id": "http-missing-security-headers",
                "matcher-name": "unknown-security-header",
                "matched-at": "http://127.0.0.1:8765",
                "info": {
                    "name": "Unknown Header",
                    "severity": "info",
                },
            }],
        })

        finding = result["findings"][0]
        self.assertIn("No se detectó el encabezado", finding["description"])
        self.assertIn("Investigar", finding["recommendation"])



    def test_analyze_scan_handles_empty_findings(self):
        result = analyze_scan({
            "target": "http://127.0.0.1:8765",
            "status": "completed",
            "findings": [],
        })

        self.assertEqual(result["raw_findings_count"], 0)
        self.assertEqual(result["grouped_findings_count"], 0)
        self.assertEqual(result["findings"], [])
        self.assertTrue(result["requires_manual_validation"])


if __name__ == "__main__":
    unittest.main()
