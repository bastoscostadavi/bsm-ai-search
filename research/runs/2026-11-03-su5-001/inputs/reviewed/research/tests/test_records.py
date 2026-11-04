"""Exercise persistence failures and recovery, without model calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).resolve().parents[1] / "tools/records.py"
spec = importlib.util.spec_from_file_location("records", TOOL)
records = importlib.util.module_from_spec(spec)
spec.loader.exec_module(records)
CAMPAIGN = TOOL.parents[1] / "campaigns/su5-benchmark.json"


class RecordsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name) / "attempt"
        records.initialize(self.run, CAMPAIGN, [])

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(TOOL), "--run", str(self.run), *args], capture_output=True, text=True)

    def test_inputs_are_snapshotted_and_attempt_cannot_be_overwritten(self):
        manifest = json.loads((self.run / "manifest.json").read_text())
        for item in manifest["input_snapshots"]:
            self.assertEqual(records.digest(self.run / item["snapshot"]), item["sha256"])
        with self.assertRaises(FileExistsError):
            records.initialize(self.run, CAMPAIGN, [])

    def test_interruption_resume_and_terminal_state_survive_new_processes(self):
        self.assertEqual(self.cli("event", "--type", "run_interrupted").returncode, 0)
        self.assertEqual(json.loads(self.cli("status").stdout)["execution_status"], "interrupted")
        self.assertNotEqual(self.cli("event", "--type", "research_note").returncode, 0)
        self.assertEqual(self.cli("event", "--type", "run_resumed").returncode, 0)
        self.assertEqual(self.cli("event", "--type", "run_completed").returncode, 0)
        self.assertNotEqual(self.cli("event", "--type", "run_resumed").returncode, 0)

    def test_concurrent_writers_preserve_unique_sequences(self):
        processes = [subprocess.Popen([sys.executable, str(TOOL), "--run", str(self.run), "event", "--type", "research_note", "--payload", json.dumps({"index": i})], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in range(8)]
        for process in processes:
            _, error = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, error)
        events = records.read_events(self.run)
        self.assertEqual([e["sequence"] for e in events], list(range(1, 10)))
        self.assertEqual(len({e["event_id"] for e in events}), 9)

    def test_command_failure_and_timeout_keep_outputs(self):
        failed = self.cli("exec", "--actor", "test", "--", sys.executable, "-c", "import sys; print('evidence'); sys.exit(7)")
        self.assertEqual(failed.returncode, 1)
        result = json.loads(failed.stdout)
        self.assertEqual(result["returncode"], 7)
        location = self.run / "commands" / result["command_id"]
        self.assertEqual((location / "stdout.log").read_text().strip(), "evidence")
        timeout = self.cli("exec", "--actor", "test", "--timeout", "0.1", "--", sys.executable, "-c", "import time; print('partial', flush=True); time.sleep(5)")
        self.assertEqual(timeout.returncode, 1)
        result = json.loads(timeout.stdout)
        self.assertTrue(result["timed_out"])
        self.assertEqual((self.run / "commands" / result["command_id"] / "stdout.log").read_text().strip(), "partial")
        self.assertEqual(records.state(records.read_events(self.run)), "running")

    def test_unfinished_command_prevents_false_completion(self):
        records.append(self.run, "test", "command_started", {"command_id": "orphan"})
        with self.assertRaises(ValueError):
            records.append(self.run, "coordinator", "run_completed", {})
        records.append(self.run, "coordinator", "command_finished", {"command_id": "orphan", "returncode": None, "recovered": True, "note": "No process remains; output unknown."})
        records.append(self.run, "coordinator", "run_completed", {})

    def test_sealing_detects_changes_additions_and_missing_files(self):
        evidence = self.run / "artifacts/result.txt"
        evidence.write_text("original")
        records.append(self.run, "coordinator", "run_completed", {})
        records.seal(self.run)
        self.assertEqual(records.verify(self.run)["execution_status"], "completed")
        evidence.write_text("changed")
        with self.assertRaises(ValueError):
            records.verify(self.run)
        evidence.write_text("original")
        extra = self.run / "extra.txt"
        extra.write_text("new")
        with self.assertRaises(ValueError):
            records.verify(self.run)
        extra.unlink()
        evidence.unlink()
        with self.assertRaises(OSError):
            records.verify(self.run)

    def test_truncated_journal_fails_visibly(self):
        with (self.run / "events.jsonl").open("a") as stream:
            stream.write('{"incomplete":')
        with self.assertRaises(ValueError):
            records.read_events(self.run)


if __name__ == "__main__":
    unittest.main()
