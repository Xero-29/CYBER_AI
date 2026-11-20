import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import execution_policy
from execution_policy import AuthorizationError, authorize_target


class ExecutionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.policy = Path(self.temp.name) / "authorizations.json"
        self.env = patch.dict(
            "os.environ",
            {"CYBER_AI_AUTHORIZATIONS_FILE": str(self.policy)},
        )
        self.env.start()
        self.grant = {
            "id": "grant-001",
            "target": "https://8.8.8.8/",
            "actions": ["nuclei_scan", "inspect_http_headers"],
            "approved_by": "security-owner",
            "ticket": "CHANGE-123",
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat(),
        }
        self.write_policy([self.grant])

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def write_policy(self, grants):
        self.policy.write_text(
            json.dumps({"authorizations": grants}),
            encoding="utf-8",
        )
        self.policy.chmod(0o600)

    def test_exact_target_and_action_grant_is_accepted(self):
        result = authorize_target(
            "https://8.8.8.8",
            "nuclei_scan",
            "grant-001",
        )
        self.assertEqual(result["ticket"], "CHANGE-123")
        self.assertEqual(result["approved_by"], "security-owner")

    def test_non_root_trailing_slash_remains_part_of_authorization_scope(self):
        self.grant["target"] = "https://8.8.8.8/api/"
        self.write_policy([self.grant])
        result = authorize_target(
            "https://8.8.8.8/api/", "nuclei_scan", "grant-001"
        )
        self.assertEqual(result["target"], "https://8.8.8.8/api/")
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8/api", "nuclei_scan", "grant-001")

    def test_wrong_target_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://1.1.1.1", "nuclei_scan", "grant-001")

    def test_wrong_action_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "arbitrary_command", "grant-001")

    def test_expired_grant_is_denied(self):
        self.grant["expires_at"] = (
            datetime.now(timezone.utc) - timedelta(minutes=1)
        ).isoformat()
        self.write_policy([self.grant])
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_hostname_is_rejected_until_dns_pinning_exists(self):
        with self.assertRaisesRegex(AuthorizationError, "IP literales"):
            authorize_target("https://example.com", "nuclei_scan", "grant-001")

    def test_private_targets_require_an_exact_explicit_grant(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("http://127.0.0.1", "nuclei_scan", "grant-001")

        self.grant["target"] = "http://127.0.0.1:8080"
        self.write_policy([self.grant])
        result = authorize_target("http://127.0.0.1:8080", "nuclei_scan", "grant-001")
        self.assertEqual(result["target"], "http://127.0.0.1:8080")

        self.grant["target"] = "http://192.168.10.20"
        self.write_policy([self.grant])
        result = authorize_target("http://192.168.10.20", "nuclei_scan", "grant-001")
        self.assertEqual(result["target"], "http://192.168.10.20")

        self.grant["target"] = "http://[fd00::1]"
        self.write_policy([self.grant])
        result = authorize_target("http://[fd00::1]", "nuclei_scan", "grant-001")
        self.assertEqual(result["target"], "http://[fd00::1]")

    def test_reserved_link_local_and_multicast_targets_are_denied(self):
        for address in ("192.0.2.1", "169.254.1.1", "224.0.0.1", "0.0.0.0"):
            with self.subTest(address=address):
                self.grant["target"] = "http://" + address
                self.write_policy([self.grant])
                with self.assertRaises(AuthorizationError):
                    authorize_target("http://" + address, "nuclei_scan", "grant-001")

    def test_grant_file_with_insecure_permissions_is_denied(self):
        self.policy.chmod(0o644)
        with self.assertRaisesRegex(AuthorizationError, "0600"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_missing_authorization_id_is_denied(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "")



    def test_duplicate_json_keys_are_rejected(self):
        self.policy.write_text(
            '{"authorizations":[],"authorizations":[]}', encoding="utf-8"
        )
        self.policy.chmod(0o600)
        with self.assertRaisesRegex(AuthorizationError, "duplicadas"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_insecure_empty_policy_remains_deny_by_default(self):
        self.write_policy([])
        self.policy.chmod(0o644)
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_insecure_policy_with_grants_is_rejected(self):
        self.policy.chmod(0o644)
        with self.assertRaisesRegex(AuthorizationError, "0600"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    @unittest.skipIf(os.name == "nt", "La propiedad POSIX no se valida en Windows.")
    def test_policy_owned_by_another_user_is_rejected(self):
        other_uid = os.geteuid() + 1
        with patch("execution_policy.os.geteuid", return_value=other_uid):
            with self.assertRaisesRegex(AuthorizationError, "pertenecer al usuario"):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    @unittest.skipIf(os.name == "nt", "Los permisos POSIX no representan ACL de Windows.")
    def test_group_writable_policy_parent_is_rejected(self):
        self.policy.parent.chmod(0o770)
        with self.assertRaisesRegex(AuthorizationError, "directorio padre"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_policy_parent_symlink_is_rejected(self):
        link = Path(self.temp.name) / "parent-link"
        try:
            link.symlink_to(self.policy.parent, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        linked_policy = link / self.policy.name
        with patch.dict("os.environ", {"CYBER_AI_AUTHORIZATIONS_FILE": str(linked_policy)}):
            with self.assertRaisesRegex(AuthorizationError, "directorio padre"):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_ancestor_symlink_is_rejected(self):
        real_root = Path(self.temp.name) / "real-root"
        nested = real_root / "nested"
        nested.mkdir(parents=True)
        real_policy = nested / "authorizations.json"
        real_policy.write_text(
            json.dumps({"authorizations": [self.grant]}), encoding="utf-8"
        )
        real_policy.chmod(0o600)
        ancestor_link = Path(self.temp.name) / "ancestor-link"
        try:
            ancestor_link.symlink_to(real_root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        linked_policy = ancestor_link / "nested" / "authorizations.json"
        with patch.dict(
            "os.environ", {"CYBER_AI_AUTHORIZATIONS_FILE": str(linked_policy)}
        ):
            with self.assertRaisesRegex(AuthorizationError, "directorio padre"):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_policy_hardlink_is_rejected(self):
        alias = Path(self.temp.name) / "authorizations-alias.json"
        try:
            os.link(self.policy, alias)
        except (OSError, NotImplementedError):
            self.skipTest("hard links unavailable")
        with self.assertRaisesRegex(AuthorizationError, "enlaces duros"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_active_authorizations_must_be_outside_repository(self):
        repository = Path(self.temp.name) / "repository"
        repository.mkdir()
        tracked_policy = repository / "authorized_targets.json"
        tracked_policy.write_text(
            json.dumps({"authorizations": [self.grant]}), encoding="utf-8"
        )
        tracked_policy.chmod(0o600)
        with patch.object(execution_policy, "PROJECT", repository):
            with patch.dict(
                "os.environ",
                {"CYBER_AI_AUTHORIZATIONS_FILE": str(tracked_policy)},
            ):
                with self.assertRaisesRegex(AuthorizationError, "fuera del repositorio"):
                    authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_policy_symlink_is_rejected(self):
        link = Path(self.temp.name) / "policy-link.json"
        try:
            link.symlink_to(self.policy)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        with patch.dict("os.environ", {"CYBER_AI_AUTHORIZATIONS_FILE": str(link)}):
            with self.assertRaisesRegex(AuthorizationError, "enlace"):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_non_regular_policy_path_is_rejected(self):
        directory = Path(self.temp.name) / "policy-directory"
        directory.mkdir()
        with patch.dict("os.environ", {"CYBER_AI_AUTHORIZATIONS_FILE": str(directory)}):
            with self.assertRaises(AuthorizationError):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO solo disponible en POSIX.")
    def test_fifo_policy_is_rejected_before_open(self):
        self.policy.unlink()
        os.mkfifo(self.policy, 0o600)
        with self.assertRaisesRegex(AuthorizationError, "archivo.*regular"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_oversized_policy_is_rejected(self):
        self.policy.write_bytes(b" " * (1024 * 1024 + 1))
        self.policy.chmod(0o600)
        with self.assertRaisesRegex(AuthorizationError, "1 MiB"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_action_string_cannot_match_by_substring(self):
        self.grant["actions"] = "prefix_nuclei_scan_suffix"
        self.write_policy([self.grant])
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_duplicate_grant_ids_are_rejected(self):
        duplicate = dict(self.grant)
        duplicate["target"] = "https://1.1.1.1"
        self.write_policy([self.grant, duplicate])
        with self.assertRaisesRegex(AuthorizationError, "identificadores duplicados"):
            authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

    def test_ambiguous_url_paths_and_zero_port_are_rejected(self):
        for target in (
            "https://8.8.8.8:0",
            "https://8.8.8.8:/",
            "https://8.8.8.8/%2e%2e/admin",
            "https://8.8.8.8/a/../admin",
            "https://8.8.8.8/a\\\\b",
        ):
            with self.subTest(target=target):
                with self.assertRaises(AuthorizationError):
                    authorize_target(target, "nuclei_scan", "grant-001")

    def test_non_string_action_and_target_are_rejected(self):
        with self.assertRaises(AuthorizationError):
            authorize_target("https://8.8.8.8", ["nuclei_scan"], "grant-001")
        with self.assertRaises(AuthorizationError):
            authorize_target(8.8, "nuclei_scan", "grant-001")


    def test_policy_replacement_during_open_is_rejected(self):
        if os.name != "posix":
            self.skipTest("La sustitución de archivo abierto se prueba en POSIX.")
        real_open = os.open

        def replace_after_open(path, flags):
            descriptor = real_open(path, flags)
            self.policy.unlink()
            self.policy.write_text(json.dumps({"authorizations": []}), encoding="utf-8")
            self.policy.chmod(0o600)
            return descriptor

        with patch("execution_policy.os.open", side_effect=replace_after_open):
            with self.assertRaisesRegex(AuthorizationError, "estable"):
                authorize_target("https://8.8.8.8", "nuclei_scan", "grant-001")

if __name__ == "__main__":
    unittest.main()
