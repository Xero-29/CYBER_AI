import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from template_integrity import (
    TemplateIntegrityError,
    hash_selected_templates,
    resolve_template_path,
    template_allowlist_id,
    verify_approved_templates,
)
from tool_allowlist import sign_tool_allowlist


class TemplateIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "nuclei-templates"
        self.template = self.root / "http" / "technologies" / "tech-detect.yaml"
        self.template.parent.mkdir(parents=True)
        self.template.write_text("id: test-template\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_hashes_only_regular_templates_inside_root(self):
        evidence = hash_selected_templates([{"path": str(self.template)}], self.root)
        self.assertEqual(evidence[0]["path"], "http/technologies/tech-detect.yaml")
        self.assertEqual(
            evidence[0]["sha256"],
            hashlib.sha256(b"id: test-template\n").hexdigest(),
        )

    def test_rejects_missing_root_with_domain_error(self):
        missing = Path(self.temp.name) / "missing-root"
        with self.assertRaises(TemplateIntegrityError):
            hash_selected_templates([{"path": str(missing / "template.yaml")}], missing)

    def test_rejects_template_outside_root(self):
        outside = Path(self.temp.name) / "outside.yaml"
        outside.write_text("id: outside\n", encoding="utf-8")
        with self.assertRaises(TemplateIntegrityError):
            resolve_template_path(outside, self.root)

    def test_rejects_path_traversal(self):
        with self.assertRaises(TemplateIntegrityError):
            resolve_template_path("../outside.yaml", self.root)

    def test_rejects_symlink_template(self):
        link = self.template.parent / "linked.yaml"
        try:
            link.symlink_to(self.template)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with self.assertRaises(TemplateIntegrityError):
            resolve_template_path(link, self.root)

    def test_rejects_symlink_directory(self):
        external = Path(self.temp.name) / "external"
        external.mkdir()
        (external / "template.yaml").write_text("id: external\n", encoding="utf-8")
        link_dir = self.root / "http" / "linked"
        try:
            link_dir.symlink_to(external, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks unavailable")
        with self.assertRaises(TemplateIntegrityError):
            resolve_template_path(link_dir / "template.yaml", self.root)

    def test_rejects_oversized_template(self):
        self.template.write_bytes(b"x" * (2 * 1024 * 1024 + 1))
        with self.assertRaises(TemplateIntegrityError):
            resolve_template_path(self.template, self.root)

    def test_template_allowlist_id_is_stable_and_rejects_traversal(self):
        first = template_allowlist_id("http/technologies/tech-detect.yaml")
        self.assertEqual(first, template_allowlist_id("http/technologies/tech-detect.yaml"))
        self.assertTrue(first.startswith("nuclei_template_"))
        self.assertLessEqual(len(first), 64)
        with self.assertRaises(TemplateIntegrityError):
            template_allowlist_id("../outside.yaml")

    def _write_signed_template_manifest(self, entries, key):
        path = Path(self.temp.name) / "tools.signed.json"
        document = sign_tool_allowlist(entries, key)
        path.write_text(
            json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        if os.name != "nt":
            path.chmod(0o600)
        return path

    def test_approved_templates_require_signed_manifest(self):
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": "",
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": "",
        }):
            with self.assertRaisesRegex(TemplateIntegrityError, "allowlist HMAC"):
                verify_approved_templates([{"path": "http/test.yaml", "sha256": "a" * 64}])

    def test_approved_templates_accept_exact_signed_path_and_hash(self):
        key = b"template-allowlist-test-key-material-32-bytes"
        relative = "http/technologies/tech-detect.yaml"
        identifier = template_allowlist_id(relative)
        manifest = self._write_signed_template_manifest(
            {identifier: {"sha256": "a" * 64}}, key
        )
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": str(manifest),
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": key.decode("utf-8"),
        }):
            result = verify_approved_templates([{"path": relative, "sha256": "a" * 64}])
        self.assertTrue(result["enforced"])
        self.assertEqual(result["approved_template_ids"], [identifier])

    def test_approved_templates_reject_hash_mismatch(self):
        key = b"template-allowlist-test-key-material-32-bytes"
        relative = "http/technologies/tech-detect.yaml"
        manifest = self._write_signed_template_manifest(
            {template_allowlist_id(relative): {"sha256": "a" * 64}}, key
        )
        with patch.dict(os.environ, {
            "CYBER_AI_TOOL_ALLOWLIST_PATH": str(manifest),
            "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": key.decode("utf-8"),
        }):
            with self.assertRaisesRegex(TemplateIntegrityError, "no está aprobada"):
                verify_approved_templates([{"path": relative, "sha256": "b" * 64}])

    def test_approved_templates_reject_manifest_inside_repository(self):
        key = b"template-allowlist-test-key-material-32-bytes"
        manifest = self.root / "tools.signed.json"
        manifest.write_text("{}", encoding="utf-8")
        with patch("template_integrity.PROJECT_ROOT", self.root):
            with patch.dict(os.environ, {
                "CYBER_AI_TOOL_ALLOWLIST_PATH": str(manifest),
                "CYBER_AI_TOOL_ALLOWLIST_HMAC_KEY": key.decode("utf-8"),
            }):
                with self.assertRaisesRegex(TemplateIntegrityError, "fuera del repositorio"):
                    verify_approved_templates([{"path": "http/test.yaml", "sha256": "a" * 64}])

    def test_rejects_hardlinked_template(self):
        with tempfile.TemporaryDirectory() as outside:
            source = Path(outside) / "source.yaml"
            source.write_text("id: linked\n", encoding="utf-8")
            linked = self.template.parent / "linked.yaml"
            try:
                os.link(source, linked)
            except OSError:
                self.skipTest("hardlinks unavailable")
            with self.assertRaises(TemplateIntegrityError):
                resolve_template_path(linked, self.root)

    def test_detects_replacement_after_open(self):
        real_open = os.open

        def replace_after_open(path, flags):
            descriptor = real_open(path, flags)
            self.template.unlink()
            self.template.write_text("id: replaced\n", encoding="utf-8")
            return descriptor

        with patch("template_integrity.os.open", side_effect=replace_after_open):
            with self.assertRaises(TemplateIntegrityError):
                hash_selected_templates([{"path": str(self.template)}], self.root)


if __name__ == "__main__":
    unittest.main()
