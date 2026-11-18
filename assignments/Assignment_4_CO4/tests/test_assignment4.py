"""Tests use only synthetic identifiers and standard-library unittest."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototype"))
from policy import Context, decide
from offline_queue import OfflineQueue, FakeServer
from audit import audit, verdict


class PolicyTests(unittest.TestCase):
    def test_known_scenarios(self):
        cases = [
            (Context(65, "wifi", charging=True), (10, "batch")),
            (Context(80, "lte", moving=True), (15, "batch")),
            (Context(20, "lte"), (120, "defer")),
            (Context(12, "lte", battery_saver=True), (180, "queue")),
            (Context(50, "offline", moving=True), (30, "queue")),
            (Context(50, "lte", hot=True), (90, "defer")),
            (Context(40, "lte", emergency=True), (5, "urgent")),
        ]
        for ctx, expected in cases:
            with self.subTest(ctx=ctx):
                d = decide(ctx)
                self.assertEqual((d.seconds, d.upload), expected)

    def test_emergency_offline_still_queues(self):
        d = decide(Context(9, "offline", emergency=True))
        self.assertEqual((d.seconds, d.upload), (5, "queue"))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Context(-2, "lte")
        with self.assertRaises(ValueError):
            Context(40, "bluetooth")


class QueueTests(unittest.TestCase):
    def test_offline_retained_and_retry_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "queue.json"
            queue = OfflineQueue(path)
            server = FakeServer()
            self.assertTrue(queue.enqueue("VISIT-A", "dummy"))
            self.assertFalse(queue.enqueue("VISIT-A", "duplicate"))
            queue.sync(server, False)
            self.assertEqual(len(server.records), 0)
            queue.sync(server, True, lose_ack_for="VISIT-A")
            self.assertEqual(queue.rows["VISIT-A"]["state"], "pending")
            self.assertEqual(len(server.records), 1)
            reloaded = OfflineQueue(path)
            reloaded.sync(server, True)
            self.assertEqual(len(server.records), 1)
            self.assertEqual(reloaded.rows["VISIT-A"]["state"], "synced")

    def test_reject_empty_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = OfflineQueue(Path(tmp) / "q.json")
            with self.assertRaises(ValueError):
                queue.enqueue("", "dummy")


class AuditTests(unittest.TestCase):
    def test_flags_distinguish_unsafe_and_safer_designs(self):
        self.assertIn("REVIEW", verdict(audit({})))
        secure = dict(https_only=True, private_token_storage=True,
                      signed_updates=True, permission_on_demand=True,
                      internal_components_exported=False)
        self.assertTrue(all(audit(secure).values()))


if __name__ == "__main__":
    unittest.main()
