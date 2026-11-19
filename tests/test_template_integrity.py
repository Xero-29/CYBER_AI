import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from template_integrity import (
    TemplateIntegrityError,
    hash_selected_templates,
    resolve_template_path,
)


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
