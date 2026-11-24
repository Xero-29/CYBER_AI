import base64
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from knowledge_pack_quality import (
    _public_https_reference,
    audit_packs,
    review_signature_payload,
)


class KnowledgePackQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.openssl = shutil.which("openssl")
        if not cls.openssl:
            raise unittest.SkipTest("OpenSSL is required for Ed25519 review-attestation tests.")
        cls.key_directory = tempfile.TemporaryDirectory(prefix="cyber-ai-test-review-")
        cls.key_root = Path(cls.key_directory.name)
        cls.private_key = cls.key_root / "reviewer-private.pem"
        cls.public_key = cls.key_root / "reviewer-public.pem"
        subprocess.run(
            [cls.openssl, "genpkey", "-algorithm", "ED25519", "-out", str(cls.private_key)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        os.chmod(cls.private_key, 0o600)
        subprocess.run(
            [
                cls.openssl, "pkey", "-in", str(cls.private_key),
                "-pubout", "-out", str(cls.public_key),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        cls.public_key_pem = cls.public_key.read_text(encoding="utf-8")
        cls.public_key_sha256 = hashlib.sha256(
            cls.public_key_pem.encode("utf-8")
        ).hexdigest()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "key_directory"):
            cls.key_directory.cleanup()

    def _review_environment(self):
        return {
            "CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_PEM": self.public_key_pem,
            "CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_SHA256": self.public_key_sha256,
            "CYBER_AI_KNOWLEDGE_REVIEWER_ID": "independent-reviewer",
        }

    def _sign_review(self, record, area_id):
        payload = review_signature_payload(record, area_id)
        payload_path = self.key_root / "review-payload.json"
        signature_path = self.key_root / "review-signature.bin"
        payload_path.write_bytes(payload)
        subprocess.run(
            [
                self.openssl, "pkeyutl", "-sign",
                "-inkey", str(self.private_key), "-rawin",
                "-in", str(payload_path), "-out", str(signature_path),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        return base64.b64encode(signature_path.read_bytes()).decode("ascii")

    @staticmethod
    def _write_json(path, value):
        path.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _sha256(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _write_expert_fixture(self, root):
        pack = root / "knowledge" / "packs" / "sample.md"
        pack.parent.mkdir(parents=True)
        headings = (
            "Propósito y límites",
            "Fundamentos",
            "Arquitectura",
            "Modelo de amenazas",
            "Competencias",
            "Mecanismos técnicos",
            "Controles",
            "Metodología",
            "Ejemplos desarrollados",
            "Laboratorio",
            "Reproducibilidad",
            "Evaluación",
            "Fuentes verificables",
            "Instrucciones para agentes IA",
        )
        pack.write_text(
            "\n".join(
                f"## {heading}\nContenido técnico reproducible."
                for heading in headings
            ) + "\n",
            encoding="utf-8",
        )

        source_evidence_dir = root / "knowledge" / "packs" / "source-evidence"
        source_evidence_dir.mkdir()
        sources = []
        for index in range(5):
            evidence_path = source_evidence_dir / f"source-{index}.txt"
            evidence_path.write_text(
                f"Revisión de metadatos, licencia y procedencia de la fuente {index}.\n",
                encoding="utf-8",
            )
            relative_evidence = evidence_path.relative_to(root).as_posix()
            sources.append({
                "id": f"source-{index}",
                "title": f"Fuente {index}",
                "publisher": "Organismo oficial",
                "url": f"https://example.org/source-{index}",
                "version": "2026-01",
                "license": "CC BY 4.0",
                "license_status": "approved",
                "verified_at": "2026-11-22T00:00:00Z",
                "verification_evidence": f"Revisión independiente {index}",
                "verification_evidence_path": relative_evidence,
                "verification_evidence_sha256": self._sha256(evidence_path),
            })

        sources_path = root / "knowledge" / "packs" / "sources.json"
        self._write_json(sources_path, {"sources": sources})

        lab_artifact = root / "knowledge" / "packs" / "lab-result.json"
        lab_artifact.write_text(
            '{"result":"passed","fixture":"deterministic"}\n',
            encoding="utf-8",
        )
        lab_path = root / "knowledge" / "packs" / "lab.json"
        self._write_json(lab_path, {
            "runs": [{
                "status": "passed",
                "artifact_path": lab_artifact.relative_to(root).as_posix(),
                "artifact_sha256": self._sha256(lab_artifact),
                "executed_at": "2026-11-22T00:00:00Z",
                "environment": "Linux isolated lab",
                "command": "pytest -q",
                "scope": "authorized local lab",
            }]
        })

        review_evidence = root / "knowledge" / "packs" / "review-evidence.txt"
        review_evidence.write_text(
            "Revisión independiente del contenido, fuentes y laboratorio.\n",
            encoding="utf-8",
        )
        review_path = root / "knowledge" / "packs" / "review.json"
        review = {
            "decision": "approved",
            "independent_review": True,
            "reviewer_id": "independent-reviewer",
            "reviewed_at": "2026-11-22T00:00:00Z",
            "reviewed_commit": "b" * 40,
            "reviewed_pack_sha256": self._sha256(pack),
            "reviewed_sources_sha256": self._sha256(sources_path),
            "reviewed_lab_evidence_sha256": self._sha256(lab_path),
            "evidence": [{
                "path": review_evidence.relative_to(root).as_posix(),
                "sha256": self._sha256(review_evidence),
            }],
        }
        review["signature"] = self._sign_review(review, "sample")
        self._write_json(review_path, review)

        manifest_path = root / "knowledge" / "packs" / "manifest.json"
        self._write_json(manifest_path, {
            "area_count": 1,
            "areas": [{
                "id": "sample",
                "name": "Sample",
                "path": pack.relative_to(root).as_posix(),
                "source_registry_path": sources_path.relative_to(root).as_posix(),
                "lab_evidence_path": lab_path.relative_to(root).as_posix(),
                "quality_review_path": review_path.relative_to(root).as_posix(),
            }],
        })
        return {
            "manifest": manifest_path,
            "pack": pack,
            "sources": sources_path,
            "source_evidence": source_evidence_dir / "source-0.txt",
            "lab": lab_path,
            "lab_artifact": lab_artifact,
            "review": review_path,
        }

    def _audit_fixture(self, manifest, environment=None):
        configured = self._review_environment() if environment is None else environment
        with patch.dict(os.environ, configured, clear=True):
            return audit_packs(manifest, root=Path(manifest).parents[2])

    def test_current_48_packs_are_not_misreported_as_expert_ready(self):
        with patch.dict(os.environ, {}, clear=True):
            report = audit_packs()
        self.assertEqual(report["status"], "audited")
        self.assertEqual(report["area_count"], 48)
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["foundation_draft_count"], 48)
        self.assertTrue(all(not item["expert_ready"] for item in report["areas"]))
        self.assertTrue(all(item["verified_external_sources"] == 0 for item in report["areas"]))
        self.assertTrue(all(
            "verified_sources_below_minimum" in item["readiness_blockers"]
            and "lab_evidence_missing_or_unverified" in item["readiness_blockers"]
            and "independent_review_missing_or_untrusted" in item["readiness_blockers"]
            for item in report["areas"]
        ))

    def test_expert_ready_requires_hashed_artifacts_and_trusted_ed25519_review(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 1)
        self.assertTrue(report["areas"][0]["expert_ready"])
        self.assertEqual(report["areas"][0]["missing_sections"], [])
        self.assertEqual(report["areas"][0]["verified_external_sources"], 5)
        self.assertEqual(report["areas"][0]["readiness_blockers"], [])

    def test_pending_source_license_prevents_expert_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            data = json.loads(fixture["sources"].read_text(encoding="utf-8"))
            data["sources"][0]["license_status"] = "pending"
            self._write_json(fixture["sources"], data)
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["areas"][0]["verified_external_sources"], 4)
        self.assertIn("verified_sources_below_minimum", report["areas"][0]["readiness_blockers"])

    def test_path_traversal_in_pack_manifest_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = self._write_expert_fixture(root)
            data = json.loads(fixture["manifest"].read_text(encoding="utf-8"))
            data["areas"][0]["path"] = "../outside.md"
            self._write_json(fixture["manifest"], data)
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["areas"][0]["quality_status"], "foundation_draft")
        self.assertIsNotNone(report["areas"][0]["path_error"])

    def test_source_evidence_hash_mismatch_is_not_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            fixture["source_evidence"].write_text("tampered evidence\n", encoding="utf-8")
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["areas"][0]["verified_external_sources"], 4)

    def test_lab_artifact_hash_mismatch_blocks_expert_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            fixture["lab_artifact"].write_text('{"result":"forged"}\n', encoding="utf-8")
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertFalse(report["areas"][0]["lab_evidence_verified"])

    def test_review_is_bound_to_exact_pack_content(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            fixture["pack"].write_text(
                fixture["pack"].read_text(encoding="utf-8") + "\nCambio posterior.\n",
                encoding="utf-8",
            )
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertFalse(report["areas"][0]["independent_review_approved"])

    def test_invalid_ed25519_signature_blocks_expert_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            review = json.loads(fixture["review"].read_text(encoding="utf-8"))
            review["signature"] = base64.b64encode(b"\x00" * 64).decode("ascii")
            self._write_json(fixture["review"], review)
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertFalse(report["areas"][0]["independent_review_approved"])

    def test_missing_or_mismatched_trusted_reviewer_key_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            report_missing = self._audit_fixture(fixture["manifest"], {})
            wrong_key = self._review_environment()
            wrong_key["CYBER_AI_KNOWLEDGE_REVIEW_PUBLIC_KEY_SHA256"] = "0" * 64
            report_wrong = self._audit_fixture(fixture["manifest"], wrong_key)
        self.assertEqual(report_missing["expert_ready_count"], 0)
        self.assertEqual(report_wrong["expert_ready_count"], 0)

    def test_private_ip_source_url_is_not_counted_as_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._write_expert_fixture(Path(directory))
            data = json.loads(fixture["sources"].read_text(encoding="utf-8"))
            data["sources"][0]["url"] = "https://127.0.0.1/private"
            self._write_json(fixture["sources"], data)
            report = self._audit_fixture(fixture["manifest"])
        self.assertEqual(report["expert_ready_count"], 0)
        self.assertEqual(report["areas"][0]["verified_external_sources"], 4)


    def test_public_https_reference_rejects_ambiguous_numeric_and_invalid_dns_hosts(self):
        invalid_urls = (
            "https://2130706433/private",
            "https://127.1/private",
            "https://0177.0.0.1/private",
            "https://0x7f000001/private",
            "https://localhost/private",
            "https://intranet/private",
            "https://bad..example.org/private",
            "https://-bad.example.org/private",
            "https://bad-.example.org/private",
            "https://example.org..private",
            "https://example.org:/source",
            "https://source.example/private",
        )
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(_public_https_reference(url))
        self.assertTrue(_public_https_reference("https://docs.example.org/reference"))


if __name__ == "__main__":
    unittest.main()
