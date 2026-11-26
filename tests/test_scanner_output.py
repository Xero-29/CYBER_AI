import os
import tempfile
import unittest
from pathlib import Path

from scanner_output import read_jsonl_findings


class ScannerOutputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "results.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def read(self, *, max_output=1024, max_line=256, max_findings=10, allow_blank=False):
        return read_jsonl_findings(
            self.path,
            max_output_bytes=max_output,
            max_line_bytes=max_line,
            max_findings=max_findings,
            allow_blank_lines=allow_blank,
        )

    def test_reads_jsonl_and_redacts_sensitive_fields(self):
        self.path.write_text(
            '{"template-id":"demo","token":"scanner-secret"}\n',
            encoding="utf-8",
        )
        findings, limited, invalid = self.read()
        self.assertFalse(limited)
        self.assertFalse(invalid)
        self.assertEqual(findings, [{"template-id": "demo", "token": "[REDACTED]"}])

    def test_missing_output_is_an_empty_result(self):
        findings, limited, invalid = self.read()
        self.assertEqual(findings, [])
        self.assertFalse(limited)
        self.assertFalse(invalid)

    def test_rejects_duplicate_json_keys(self):
        self.path.write_text('{"id":"first","id":"second"}\n', encoding="utf-8")
        self.assertEqual(self.read(), ([], False, True))

    def test_rejects_non_finite_json_constants(self):
        self.path.write_text('{"score":NaN}\n', encoding="utf-8")
        self.assertEqual(self.read(), ([], False, True))

    def test_rejects_non_object_json_records(self):
        self.path.write_text('[{"id":"not-an-object-record"}]\n', encoding="utf-8")
        self.assertEqual(self.read(), ([], False, True))

    def test_rejects_invalid_utf8(self):
        self.path.write_bytes(b'{"id":"\xff"}\n')
        self.assertEqual(self.read(), ([], False, True))

    def test_output_size_limit_is_enforced_before_parsing(self):
        self.path.write_bytes(b'{"id":1}\n')
        self.assertEqual(self.read(max_output=4), ([], True, False))

    def test_line_size_limit_is_enforced(self):
        self.path.write_text('{"id":"long"}\n', encoding="utf-8")
        self.assertEqual(self.read(max_line=5), ([], False, True))

    def test_finding_count_limit_discards_partial_results(self):
        self.path.write_text('{"id":1}\n{"id":2}\n', encoding="utf-8")
        self.assertEqual(self.read(max_findings=1), ([], True, False))

    def test_blank_lines_are_rejected_by_default_and_can_be_skipped_explicitly(self):
        self.path.write_text('{"id":1}\n\n', encoding="utf-8")
        self.assertEqual(self.read(), ([], False, True))
        self.assertEqual(self.read(allow_blank=True), ([{"id": 1}], False, False))

    def test_symlink_output_is_rejected(self):
        outside = Path(self.temp.name) / "outside.jsonl"
        outside.write_text('{"id":1}\n', encoding="utf-8")
        try:
            self.path.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.assertEqual(self.read(), ([], False, True))

    @unittest.skipUnless(os.name == "posix", "hardlink checks are POSIX-specific")
    def test_hardlinked_output_is_rejected(self):
        outside = Path(self.temp.name) / "outside.jsonl"
        outside.write_text('{"id":1}\n', encoding="utf-8")
        os.link(outside, self.path)
        self.assertEqual(self.read(), ([], False, True))


if __name__ == "__main__":
    unittest.main()
