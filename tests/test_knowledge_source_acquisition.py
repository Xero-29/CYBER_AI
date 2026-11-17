import json, tempfile, unittest
from pathlib import Path
import knowledge_source_acquisition as intake

class SourceAcquisitionTests(unittest.TestCase):
    def test_curated_catalog_is_valid_and_disabled(self):
        data=intake.load_sources()
        report=intake.audit(data)
        self.assertTrue(report["ok"])
        self.assertGreaterEqual(report["source_count"],10)
        catalog=intake.build_downloader_catalog(data)
        self.assertTrue(catalog["resources"])
        self.assertTrue(all(x["verified_for_download"] is False and x["download"] is False for x in catalog["resources"]))
    def test_rejects_http_and_credentials(self):
        data={"schema_version":"1.0.0","sources":[{"id":"unsafe-source","title":"x","publisher":"x","url":"http://example.org/a","landing_url":"https://example.org","type":"standard","license":"unknown","license_url":"https://example.org/license","areas":["foundations"],"format":"pdf","cadence":"annual"}]}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"sources.json"; path.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(ValueError): intake.load_sources(path)
    def test_rejects_duplicate_ids(self):
        data=intake.load_sources(); data["sources"].append(dict(data["sources"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"sources.json"; path.write_text(json.dumps(data),encoding="utf-8")
            with self.assertRaises(ValueError): intake.load_sources(path)
if __name__=="__main__": unittest.main()
