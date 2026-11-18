import json
import tempfile
import unittest
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch
import subprocess

import tool_database_preflight as preflight


class ToolDatabasePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def _osv_bundle(self, root, ecosystem="PyPI"):
        db = root / "osv-scalibr" / ecosystem
        db.mkdir(parents=True)
        with zipfile.ZipFile(db / "all.zip", "w") as archive:
            archive.writestr("OSV-2026-1.json", '{"id":"OSV-2026-1"}')
        return db / "all.zip"

    def test_osv_preflight_detects_valid_local_ecosystem_archives(self):
        self._osv_bundle(self.root)
        result = preflight.inspect_osv_database(
            environ={"OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY": str(self.root)},
            home=self.root / "home",
            temp_dir=self.root / "tmp",
        )
        self.assertEqual(result["status"], "present_structure_checked")
        self.assertEqual(result["ecosystems"], ["PyPI"])
        self.assertEqual(result["freshness"], "unknown")
        self.assertEqual(result["schema_validation"], "not_exposed_by_documented_all_zip_layout")
        self.assertFalse(result["network_access"])

    def test_osv_preflight_fails_when_database_is_missing(self):
        result = preflight.inspect_osv_database(
            environ={"OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY": str(self.root)},
            home=self.root / "home",
            temp_dir=self.root / "tmp",
        )
        self.assertEqual(result["status"], "missing")

    def test_osv_preflight_ignores_corrupt_and_empty_archives(self):
        db = self.root / "osv-scalibr" / "npm"
        db.mkdir(parents=True)
        (db / "all.zip").write_bytes(b"not a zip")
        result = preflight.inspect_osv_database(
            environ={"OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY": str(self.root)},
            home=self.root / "home",
            temp_dir=self.root / "tmp",
        )
        self.assertEqual(result["status"], "missing_or_invalid")

    def test_osv_preflight_rejects_symlinked_database_directory(self):
        actual = self.root / "actual"
        actual.mkdir()
        link = self.root / "osv-scalibr"
        link.symlink_to(actual, target_is_directory=True)
        result = preflight.inspect_osv_database(
            environ={"OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY": str(self.root)},
            home=self.root / "home",
            temp_dir=self.root / "tmp",
        )
        self.assertEqual(result["status"], "missing")

    def _grype_status(self, *, built=None, schema="6.1.3", error=None, status=None, path=None):
        db = self.root / "vulnerability.db"
        db.write_bytes(b"sqlite fixture")
        payload = {
            "schemaVersion": schema,
            "built": built or datetime.now(timezone.utc).isoformat(),
            "path": str(path or db),
            "error": error,
        }
        if status is not None:
            payload["status"] = status
        return subprocess.CompletedProcess(
            ["grype", "db", "status", "--output", "json"],
            0, stdout=json.dumps(payload), stderr="",
        )

    @patch("tool_database_preflight.subprocess.run")
    def test_grype_preflight_accepts_valid_recent_database_and_disables_network(self, run):
        run.return_value = self._grype_status()
        result = preflight.inspect_grype_database(
            "/usr/bin/grype", environ={"PATH": "/usr/bin", "HOME": str(self.root)}
        )
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["schema_version"], "6.1.3")
        env = run.call_args.kwargs["env"]
        self.assertEqual(env["GRYPE_DB_AUTO_UPDATE"], "false")
        self.assertEqual(env["GRYPE_EXTERNAL_SOURCES_ENABLE"], "false")
        self.assertEqual(env["GRYPE_CHECK_FOR_APP_UPDATE"], "false")
        self.assertFalse(run.call_args.kwargs["shell"])

    @patch("tool_database_preflight.subprocess.run")
    def test_grype_preflight_rejects_stale_database(self, run):
        old = (datetime.now(timezone.utc) - timedelta(days=20)).isoformat()
        run.return_value = self._grype_status(built=old)
        result = preflight.inspect_grype_database(
            "/usr/bin/grype", environ={"PATH": "/usr/bin", "HOME": str(self.root)}
        )
        self.assertEqual(result["status"], "stale")
        self.assertEqual(result["max_age_days"], preflight.DEFAULT_GRYPE_MAX_AGE_DAYS)

    @patch("tool_database_preflight.subprocess.run")
    def test_grype_preflight_rejects_invalid_schema_and_error_status(self, run):
        run.return_value = self._grype_status(schema="unknown")
        result = preflight.inspect_grype_database("/usr/bin/grype")
        self.assertEqual(result["status"], "invalid_metadata")
        run.return_value = self._grype_status(error="checksum mismatch")
        result = preflight.inspect_grype_database("/usr/bin/grype")
        self.assertEqual(result["status"], "invalid_database")

    @patch("tool_database_preflight.subprocess.run")
    def test_grype_preflight_rejects_missing_database_file(self, run):
        run.return_value = self._grype_status(path=self.root / "absent.db")
        result = preflight.inspect_grype_database("/usr/bin/grype")
        self.assertEqual(result["status"], "missing_or_invalid")

    def test_grype_age_policy_is_bounded(self):
        for value in ("0", "3651", "one"):
            with self.assertRaises(ValueError):
                preflight.inspect_grype_database(
                    "/usr/bin/grype",
                    environ={"CYBER_AI_GRYPE_DB_MAX_AGE_DAYS": value},
                )


if __name__ == "__main__":
    unittest.main()
