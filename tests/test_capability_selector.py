import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import capability_selector


class CapabilitySelectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory = self.root / "reports" / "capability_inventory.json"
        self.templates = self.root / "nuclei-templates"
        template = self.templates / "http" / "technologies" / "tech-detect.yaml"
        template.parent.mkdir(parents=True)
        template.write_text("id: tech-detect\ninfo:\n  tags: tech,detect\n", encoding="utf-8")
        self.item = {
            "name": "tech-detect",
            "path": str(template),
            "category": "technologies",
        }
        self.inventory_patch = patch.object(
            capability_selector, "INVENTORY", self.inventory
        )
        self.template_patch = patch.object(
            capability_selector, "TEMPLATE_ROOT", self.templates
        )
        self.inventory_patch.start()
        self.template_patch.start()

    def tearDown(self):
        self.template_patch.stop()
        self.inventory_patch.stop()
        self.temp.cleanup()

    def test_missing_inventory_discovers_in_memory_without_writing_cache(self):
        with patch.object(
            capability_selector,
            "build_inventory",
            return_value={"nuclei_templates": {"items": [self.item]}},
        ) as discover:
            results = capability_selector.select_capabilities("auditoria de seguridad")
        discover.assert_called_once_with()
        self.assertEqual([item["name"] for item in results], ["tech-detect"])
        self.assertFalse(self.inventory.exists())

    def test_existing_inventory_is_used_without_discovery(self):
        self.inventory.parent.mkdir(parents=True)
        self.inventory.write_text(
            json.dumps({"nuclei_templates": {"items": [self.item]}}),
            encoding="utf-8",
        )
        with patch.object(capability_selector, "build_inventory") as discover:
            results = capability_selector.select_capabilities("auditoria general")
        discover.assert_not_called()
        self.assertEqual(len(results), 1)

    def test_symlinked_inventory_is_rejected(self):
        self.inventory.parent.mkdir(parents=True)
        real = self.root / "real-inventory.json"
        real.write_text(json.dumps({"nuclei_templates": {"items": []}}), encoding="utf-8")
        try:
            self.inventory.symlink_to(real)
        except (OSError, NotImplementedError):
            self.skipTest("El sistema de archivos no permite crear symlinks.")
        with self.assertRaisesRegex(ValueError, "symlink"):
            capability_selector.select_capabilities("auditoria")

    def test_template_paths_outside_root_are_ignored(self):
        outside = self.root / "outside.yaml"
        outside.write_text("id: outside\n", encoding="utf-8")
        with patch.object(
            capability_selector,
            "build_inventory",
            return_value={"nuclei_templates": {"items": [{
                "name": "outside", "path": str(outside), "category": "technologies"
            }]}},
        ):
            self.assertEqual(
                capability_selector.select_capabilities("auditoria de seguridad"),
                [],
            )

    def test_empty_task_and_invalid_limits_are_rejected(self):
        for task in ("", "  ", None):
            with self.subTest(task=task), self.assertRaises(ValueError):
                capability_selector.select_capabilities(task)
        for limit in (True, 0, -1, 101, 1.5, "5"):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                capability_selector.select_capabilities("auditoria", limit=limit)


if __name__ == "__main__":
    unittest.main()
