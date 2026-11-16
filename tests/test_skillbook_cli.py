import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import skillbook_cli


class SkillbookCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.manifest = Path(self.temp.name) / "skill.json"
        self.data = {
            "name": "Prueba",
            "task_pattern": "auditoria segura",
            "description": "Metodología reproducible",
            "prerequisites": [],
            "methodology": ["preparar entorno", "ejecutar comprobación"],
            "validation": ["verificar evidencia"],
            "tools": ["ruff"],
            "tags": ["test"],
            "source_urls": ["https://example.org/"],
            "namespace": "nexo",
            "event_ids": ["run-1", "run-2"],
        }
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_propose_calls_verified_ledger_api(self):
        with patch.object(skillbook_cli.skillbook, "propose_skill_from_ledger",
                          return_value={"status": "candidate"}) as propose, \
             patch("builtins.print"):
            result = skillbook_cli.main(["propose", "--manifest", str(self.manifest)])
        self.assertEqual(result, 0)
        propose.assert_called_once_with(**self.data)

    def test_manifest_rejects_unknown_fields(self):
        self.data["approval"] = "self asserted"
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")
        with patch("builtins.print"):
            result = skillbook_cli.main(["propose", "--manifest", str(self.manifest)])
        self.assertEqual(result, 2)

    def test_manifest_rejects_symlink(self):
        link = Path(self.temp.name) / "link.json"
        link.symlink_to(self.manifest)
        with patch("builtins.print"):
            result = skillbook_cli.main(["propose", "--manifest", str(link)])
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
