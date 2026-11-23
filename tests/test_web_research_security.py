import json
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

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



class WebResearchEgressSecurityTests(unittest.TestCase):
    def setUp(self):
        self.sources = [{
            "id": "official",
            "name": "Official",
            "domains": ["example.org"],
            "tier": 1,
            "limitations": "Test source",
        }]

    def test_source_registry_rejects_broad_local_and_ambiguous_domains(self):
        invalid_domains = (
            ["com"],
            ["localhost"],
            ["127.0.0.1"],
            ["2130706433"],
            ["127.1"],
            ["*.example.org"],
            ["example.org/path"],
            ["bad..example.org"],
            ["-bad.example.org"],
        )
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "trusted-sources.json"
            for domains in invalid_domains:
                with self.subTest(domains=domains):
                    config_path.write_text(
                        json.dumps({"sources": [{"id": "test", "domains": domains}]}),
                        encoding="utf-8",
                    )
                    with patch.object(web_research, "CONFIG_PATH", config_path):
                        with self.assertRaisesRegex(ValueError, "dominio|DNS|fuentes"):
                            web_research.load_sources()

    def test_source_registry_normalizes_valid_idna_domains(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "trusted-sources.json"
            config_path.write_text(
                json.dumps({
                    "sources": [{
                        "id": "official",
                        "domains": ["EXAMPLE.ORG.", "exämple.org"],
                    }]
                }),
                encoding="utf-8",
            )
            with patch.object(web_research, "CONFIG_PATH", config_path):
                _, sources = web_research.load_sources()
        self.assertEqual(
            sources[0]["domains"],
            ["example.org", "xn--exmple-cua.org"],
        )

    def test_missing_proxy_blocks_search_before_network(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(web_research, "load_sources", return_value=({}, self.sources)):
                with patch.object(web_research, "DDGS") as ddgs:
                    with self.assertRaisesRegex(ValueError, web_research.WEB_RESEARCH_PROXY_ENV):
                        web_research.search_web("non-sensitive test query")
        ddgs.assert_not_called()

    def test_search_request_rejects_invalid_query_before_loading_policy_or_network(self):
        invalid_queries = (
            None,
            1,
            "",
            " \t ",
            "x" * (web_research.MAX_SEARCH_QUERY_CHARS + 1),
            "two\nlines",
            "nul\x00byte",
            "control\x85char",
        )
        for query in invalid_queries:
            with self.subTest(query=repr(query)):
                with patch.object(web_research, "load_sources") as load_sources:
                    with patch.object(web_research, "_validated_web_egress_proxy") as proxy:
                        with patch.object(web_research, "DDGS") as ddgs:
                            with self.assertRaises(ValueError):
                                web_research.search_web(query)
                load_sources.assert_not_called()
                proxy.assert_not_called()
                ddgs.assert_not_called()

    def test_search_request_rejects_invalid_options_before_loading_policy(self):
        invalid_limits = (True, False, 0, -1, 21, 1.5, "5", None)
        for limit in invalid_limits:
            with self.subTest(max_results=repr(limit)):
                with patch.object(web_research, "load_sources") as load_sources:
                    with self.assertRaises(ValueError):
                        web_research.search_web("valid query", max_results=limit)
                load_sources.assert_not_called()

        invalid_untrusted_flags = (1, 0, "true", None)
        for flag in invalid_untrusted_flags:
            with self.subTest(include_untrusted=repr(flag)):
                with patch.object(web_research, "load_sources") as load_sources:
                    with self.assertRaises(ValueError):
                        web_research.search_web("valid query", include_untrusted=flag)
                load_sources.assert_not_called()

    def test_search_request_trims_query_and_accepts_explicit_bounded_options(self):
        proxy = "http://127.0.0.1:8080"
        with patch.dict(os.environ, {web_research.WEB_RESEARCH_PROXY_ENV: proxy}):
            with patch.object(web_research, "load_sources", return_value=({}, self.sources)):
                with patch.object(web_research, "DDGS") as ddgs:
                    ddgs.return_value.text.return_value = []
                    report = web_research.search_web(
                        "  valid query  ",
                        max_results=web_research.MAX_SEARCH_RESULTS,
                        include_untrusted=True,
                    )
        self.assertEqual(report["query"], "valid query")
        self.assertFalse(report["trusted_only"])
        ddgs.return_value.text.assert_any_call(
            "valid query",
            max_results=web_research.MAX_SEARCH_RESULTS,
            region="us-en",
            safesearch="moderate",
            backend="auto",
        )

    def test_proxy_validation_rejects_plaintext_remote_and_credentials(self):
        invalid = (
            "http://proxy.example.org:8080",
            "http://user:password@127.0.0.1:8080",
            "https://proxy.example.org:8443/path",
            "https://proxy.example.org:8443/?token=secret",
            "http://127.0.0.1:0",
        )
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    web_research._validate_web_egress_proxy(value)

    def test_proxy_validation_accepts_loopback_http_and_remote_https(self):
        self.assertEqual(
            web_research._validate_web_egress_proxy("http://127.0.0.1:8080"),
            "http://127.0.0.1:8080",
        )
        self.assertEqual(
            web_research._validate_web_egress_proxy("https://egress.example.org:8443"),
            "https://egress.example.org:8443",
        )

    def test_search_and_page_fetch_use_the_same_explicit_proxy(self):
        proxy = "http://127.0.0.1:8080"
        result_item = {
            "href": "https://example.org/advisory",
            "title": "Advisory",
            "body": "Summary",
            "date": None,
        }
        with patch.dict(os.environ, {web_research.WEB_RESEARCH_PROXY_ENV: proxy}):
            with patch.object(web_research, "load_sources", return_value=({}, self.sources)):
                with patch.object(web_research, "DDGS") as ddgs:
                    ddgs.return_value.text.return_value = [result_item]
                    with patch.object(
                        web_research, "fetch_trusted_page",
                        return_value={"fetch_status": "pagina consultada"},
                    ) as fetch:
                        report = web_research.search_web("non-sensitive test query")
        ddgs.assert_called_once_with(proxy=proxy, timeout=8)
        fetch.assert_called_once_with(result_item["href"], self.sources, proxy=proxy)
        self.assertEqual(report["search_status"], "ok")
        self.assertEqual(report["results"][0]["fetch_status"], "pagina consultada")

    def test_trusted_domain_matching_rejects_ambiguous_url_authorities(self):
        invalid_urls = (
            "https://@example.org/advisory",
            "https://2130706433/advisory",
            "https://127.1/advisory",
            "https://example.org:/advisory",
            "https://example.org:0/advisory",
            "https://example.org:99999/advisory",
            "https://user:secret@example.org/advisory",
            "https://example.org/advisory\nforged",
            "https://example.org/advisory\x85forged",
            "https://example.org/" + ("x" * web_research.MAX_RESEARCH_URL_CHARS),
            None,
        )
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertIsNone(web_research.trusted_domain_for_url(url, self.sources))
        self.assertIsNotNone(
            web_research.trusted_domain_for_url("https://docs.example.org/advisory", self.sources)
        )

    def test_page_fetch_rejects_oversized_url_before_opening_connection(self):
        proxy = "http://127.0.0.1:8080"
        url = "https://example.org/" + ("x" * web_research.MAX_RESEARCH_URL_CHARS)
        with patch.object(web_research, "build_opener") as build:
            result = web_research.fetch_trusted_page(url, self.sources, proxy=proxy)
        self.assertEqual(result["fetch_status"], "omitida: dominio no registrado")
        build.assert_not_called()

    def test_page_fetch_installs_explicit_proxy_and_rejects_http_sources(self):
        proxy = "http://127.0.0.1:8080"

        class Headers:
            def get(self, name, default=None):
                return "text/html; charset=utf-8" if name.lower() == "content-type" else default

            def get_content_charset(self):
                return "utf-8"

        class Response:
            headers = Headers()

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def geturl(self):
                return "https://example.org/advisory"

            def read(self, limit):
                return b"<html><title>Advisory</title><p>Evidence</p></html>"

        opener = Mock()
        opener.open.return_value = Response()
        with patch.object(web_research, "build_opener", return_value=opener) as build:
            result = web_research.fetch_trusted_page(
                "https://example.org/advisory", self.sources, proxy=proxy
            )
        handlers = build.call_args.args
        self.assertIsInstance(handlers[0], web_research.ProxyHandler)
        self.assertEqual(handlers[0].proxies, {"http": proxy, "https": proxy})
        self.assertIsInstance(handlers[1], web_research.TrustedRedirectHandler)
        self.assertEqual(result["fetch_status"], "pagina consultada")
        self.assertIsNone(web_research.trusted_domain_for_url("http://example.org/advisory", self.sources))


if __name__ == "__main__":
    unittest.main()
