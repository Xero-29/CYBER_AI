import json
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import web_research


class WebResearchOutputSecurityTests(unittest.TestCase):
    def test_report_files_are_private_and_redact_sensitive_content(self):
        with tempfile.TemporaryDirectory() as directory:
            report_dir = Path(directory) / "research"
            secret = "research-provider-secret"
            report = {
                "query": f"token={secret}",
                "retrieved_at_utc": "2026-11-22T00:00:00+00:00",
                "trusted_only": True,
                "registered_source_count": 1,
                "search_status": "ok",
                "backend_used": "test",
                "successful_backends": 1,
                "results": [{
                    "title": "Resultado",
                    "source_name": "Fuente",
                    "tier": 1,
                    "url": f"https://example.org/doc?X-Amz-Signature={secret}",
                    "published_at": None,
                    "modified_at": None,
                    "fetch_status": "ok",
                    "search_snippet": f"password={secret}",
                    "page_title": "Página",
                    "page_text": f"api_key={secret}",
                    "source_limitations": None,
                }],
            }
            with patch.object(web_research, "REPORT_DIR", report_dir):
                md_path, json_path = web_research.write_report(report)

            for path in (md_path, json_path):
                rendered = path.read_text(encoding="utf-8")
                self.assertNotIn(secret, rendered)
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(report_dir.stat().st_mode), 0o700)
            parsed = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(parsed["query"], "token=[REDACTED]")

    def test_cli_redacts_provider_errors(self):
        secret = "research-cli-secret"
        output = StringIO()
        with patch("sys.argv", ["web_research.py", "prueba"]), patch.object(
            web_research, "search_web",
            side_effect=RuntimeError(f"falló el proveedor token={secret}"),
        ), redirect_stderr(output):
            result = web_research.main()
        self.assertEqual(result, 1)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())


if __name__ == "__main__":
    unittest.main()
