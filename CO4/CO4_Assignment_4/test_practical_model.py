import unittest
from practical_model import Context, model_startup, sync_decision


class PolicyTests(unittest.TestCase):
    def test_permission_not_bypassed(self):
        self.assertEqual(sync_decision(Context(True, 90, True, True), True, False), "REJECT: no permission")

    def test_encryption_enforced(self):
        self.assertIn("unencrypted", sync_decision(Context(True, 90, True, True), False, True))

    def test_offline_deferred(self):
        self.assertEqual(sync_decision(Context(False, 90, True, True), True, True), "DEFER: offline")

    def test_background_uses_worker(self):
        self.assertEqual(sync_decision(Context(True, 60, False, False), True, True), "SCHEDULE: OS-managed worker")

    def test_invalid_battery(self):
        with self.assertRaises(ValueError):
            Context(True, 120, False, True)

    def test_cold_model_more_expensive(self):
        self.assertGreater(model_startup(True), model_startup(False))


if __name__ == "__main__":
    unittest.main()
