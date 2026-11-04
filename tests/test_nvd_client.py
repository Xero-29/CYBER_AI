import unittest
from unittest.mock import patch

from nvd_client import enrich_analysis, verify_cve


class NVDClientTests(unittest.TestCase):
    @patch("nvd_client.urllib.request.urlopen")
    def test_exact_cve_found(self, mock_urlopen):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return b'{"vulnerabilities":[{"cve":{"id":"CVE-2024-12345","vulnStatus":"Analyzed","descriptions":[{"lang":"en","value":"Test CVE"}]}}]}'

        mock_urlopen.return_value = FakeResponse()
        result = verify_cve("CVE-2024-12345")
        self.assertEqual(result["status"], "found_in_nvd")
        self.assertEqual(result["patch_status"], "unverified")

    @patch("nvd_client.urllib.request.urlopen", side_effect=OSError("offline"))
    def test_network_failure_remains_pending(self, mock_urlopen):
        result = verify_cve("CVE-2024-12345")
        self.assertEqual(result["status"], "verification_pending")

    def test_no_cves_means_no_network_checks(self):
        result = enrich_analysis({"cve_references": []})
        self.assertEqual(result["nvd_checks"], [])
        self.assertFalse(result["confirmed_vulnerability"])


if __name__ == "__main__":
    unittest.main()
