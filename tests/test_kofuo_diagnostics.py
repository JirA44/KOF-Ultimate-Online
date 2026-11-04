"""Portable unit tests for the per-launch KOFUO diagnostic reporter."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kofuo_diagnostics import DiagnosticRun


class DiagnosticRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.game = self.root / "game"
        self.game.mkdir()
        self.exe = self.game / "KOF_Ultimate_Online.exe"
        self.exe.write_bytes(b"test fixture only")
        self.log = self.game / "mugen.log"
        self.log.write_text("previous run\n", encoding="utf-8")
        self.local = self.root / "local"
        self.outbox = self.root / "shared"
        self.env = patch.dict(os.environ, {
            "KOFUO_DIAGNOSTICS_LOCAL_DIR": str(self.local),
            "KOFUO_DIAGNOSTICS_OUTBOX": str(self.outbox),
        })
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def test_exit_writes_local_report_and_redacted_shared_report(self):
        run = DiagnosticRun(self.game, self.exe)
        self.log.write_text(
            "ERROR detected at C:\\Users\\alice\\private.dat password=hidden\n",
            encoding="utf-8",
        )
        result = run.finish(1)
        local_path = self.local / "reports" / f"{run.report_id}.json"
        shared_path = self.outbox / f"{run.report_id}.json"
        local_report = json.loads(local_path.read_text(encoding="utf-8"))
        shared_report = json.loads(shared_path.read_text(encoding="utf-8"))

        self.assertEqual(result["status"], "nonzero_exit")
        self.assertTrue(local_report["raw_log_saved_locally"])
        self.assertFalse(shared_report["raw_log_uploaded"])
        self.assertEqual(shared_report["supa_delivery"], "shared_folder_outbox")
        excerpt = " ".join(shared_report["error_excerpt"])
        self.assertNotIn("hidden", excerpt)
        self.assertNotIn("C:\\Users\\alice", excerpt)
        self.assertTrue((self.local / "raw_logs" / f"{run.report_id}.log").exists())

    def test_launch_failure_is_reported_without_running_game(self):
        run = DiagnosticRun(self.game, self.exe)
        result = run.finish(None, launch_error="game_executable_missing")
        self.assertEqual(result["status"], "launch_failed")
        self.assertIn("launch_failed", result["signals"])
        self.assertTrue((self.local / "reports" / f"{run.report_id}.json").exists())


if __name__ == "__main__":
    unittest.main()
