import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import knowledge_downloader as downloader


class KnowledgeDownloaderSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root_patch = patch.object(downloader, "ROOT", Path(self.temp.name))
        self.root_patch.start()
        self.base_patch = patch.object(downloader, "BASE", Path(self.temp.name) / "base")
        self.base_patch.start()

    def tearDown(self):
        self.base_patch.stop()
        self.root_patch.stop()
        self.temp.cleanup()

    def item(self, **overrides):
        item = {
            "id": "docs-example",
            "url": "https://docs.example.org/file.txt",
            "folder": "docs",
            "filename": "file.txt",
            "max_bytes": 1024,
            "verified_for_download": True,
        }
        item.update(overrides)
        return item

    @patch.object(downloader.socket, "getaddrinfo")
    def test_rejects_plain_http(self, resolver):
        with self.assertRaises(ValueError):
            downloader._validate_public_https("http://docs.example.org/file")
        resolver.assert_not_called()

    @patch.object(downloader.socket, "getaddrinfo")
    def test_rejects_loopback_and_private_addresses(self, resolver):
        resolver.return_value = [(None, None, None, None, ("127.0.0.1", 443))]
        with self.assertRaises(ValueError):
            downloader._validate_public_https("https://docs.example.org/file")

    @patch.object(downloader.socket, "getaddrinfo")
    def test_rejects_redirect_to_another_host(self, resolver):
        resolver.return_value = [(None, None, None, None, ("93.184.216.34", 443))]
        with self.assertRaises(ValueError):
            downloader._validate_public_https(
                "https://attacker.example/file",
                expected_host="docs.example.org",
            )

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            downloader._safe_destination(self.item(folder="../outside"))
        with self.assertRaises(ValueError):
            downloader._safe_destination(self.item(filename="../outside.txt"))

    def test_rejects_symlink_destination(self):
        base = downloader.BASE
        base.mkdir(parents=True)
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (base / "docs").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            downloader._safe_destination(self.item())

    @patch.object(downloader.socket, "getaddrinfo")
    @patch.object(downloader.requests, "Session")
    def test_download_uses_no_proxy_and_rejects_cross_host_redirect(self, session_factory, resolver):
        resolver.return_value = [(None, None, None, None, ("93.184.216.34", 443))]
        session = MagicMock()
        session.trust_env = True
        response = MagicMock()
        response.status_code = 302
        response.headers = {"Location": "https://other.example/file"}
        session.get.return_value = response
        session_factory.return_value = session

        with self.assertRaises(ValueError):
            downloader.download(self.item(), {"resources": {}})
        self.assertFalse(session.trust_env)
        session.get.assert_called_once()
        self.assertFalse(session.get.call_args.kwargs["allow_redirects"])

    @patch.object(downloader.socket, "getaddrinfo")
    def test_dry_run_does_not_create_file(self, resolver):
        resolver.return_value = [(None, None, None, None, ("93.184.216.34", 443))]
        manifest = {"resources": {}}
        result = downloader.download(self.item(), manifest, dry_run=True)
        self.assertEqual(result, "dry_run")
        self.assertFalse((downloader.BASE / "docs").exists())
        self.assertEqual(manifest["resources"], {})
        resolver.assert_not_called()


if __name__ == "__main__":
    unittest.main()
