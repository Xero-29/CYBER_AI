import hashlib
import os
import stat
import tempfile
import unittest
import uuid
import zlib
from pathlib import Path
from unittest.mock import patch

import compressed_store as store


class CompressedStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cyber-ai-compressed-store-")
        self.original_path = store.DB_PATH
        store.DB_PATH = Path(self.temp.name) / "blocks.sqlite3"

    def tearDown(self):
        store.DB_PATH = self.original_path
        self.temp.cleanup()

    def test_round_trip_preserves_content_and_metadata(self):
        saved = store.store_block(
            content="evidencia comprimida",
            session_id="session-a",
            task_id="task-1",
            metadata={"classification": "internal"},
        )
        recovered = store.read_block(saved["id"], "session-a")
        self.assertEqual(recovered["content"], "evidencia comprimida")
        self.assertEqual(recovered["metadata"], {"classification": "internal"})
        self.assertEqual(store.list_blocks("session-a")[0]["id"], saved["id"])

    def test_database_file_is_private_on_posix(self):
        store.initialize()
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(store.DB_PATH.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(store.DB_PATH.parent.stat().st_mode), 0o700)

    def test_oversized_content_is_rejected_before_storage(self):
        with patch.object(store, "MAX_BLOCK_BYTES", 3):
            with self.assertRaisesRegex(ValueError, "2 MiB"):
                store.store_block(content="four", session_id="session-a")

    def test_non_finite_metadata_is_rejected(self):
        with self.assertRaises(ValueError):
            store.store_block(
                content="safe",
                session_id="session-a",
                metadata={"score": float("nan")},
            )

    def test_list_limit_is_strict(self):
        for limit in (True, "10", 0, 101, 1.5):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "limit"):
                store.list_blocks("session-a", limit=limit)

    def test_read_rejects_declared_oversized_block_before_decompression(self):
        saved = store.store_block(content="safe", session_id="session-a")
        store.initialize()
        with store.database() as db:
            db.execute(
                "UPDATE compressed_blocks SET original_bytes=? WHERE id=?",
                (store.MAX_BLOCK_BYTES + 1, saved["id"]),
            )
        with self.assertRaisesRegex(ValueError, "tamaños declarados"):
            store.read_block(saved["id"], "session-a")

    def test_read_bounds_decompression_even_if_declared_size_is_forged(self):
        store.initialize()
        raw = b"x" * (store.MAX_BLOCK_BYTES + 1)
        compressed = zlib.compress(raw)
        block_id = uuid.uuid4().hex
        with store.database() as db:
            db.execute(
                """INSERT INTO compressed_blocks (
                    id, session_id, task_id, kind, compressed_data, sha256,
                    original_bytes, compressed_bytes, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    block_id, "session-a", None, "note", compressed,
                    hashlib.sha256(raw).hexdigest(), 1, len(compressed), "{}",
                    store.utc_now(),
                ),
            )
        with self.assertRaisesRegex(ValueError, "excede los límites"):
            store.read_block(block_id, "session-a")

    def test_read_rejects_duplicate_metadata_keys(self):
        saved = store.store_block(
            content="safe", session_id="session-a", metadata={"a": 1}
        )
        with store.database() as db:
            db.execute(
                "UPDATE compressed_blocks SET metadata_json=? WHERE id=?",
                ('{"a":1,"a":2}', saved["id"]),
            )
        with self.assertRaisesRegex(ValueError, "claves duplicadas"):
            store.read_block(saved["id"], "session-a")


if __name__ == "__main__":
    unittest.main()
