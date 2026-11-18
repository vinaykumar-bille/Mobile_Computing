"""Tests for the illustrative CO4 mobile policy simulations."""
import unittest
from mobile_lab import DeviceContext, Inbox, allow_sync, startup_model, permission_decision


class MobileLabTests(unittest.TestCase):
    def test_offline_blocks_sync(self):
        self.assertFalse(allow_sync(DeviceContext(False, 90, True, True)))

    def test_low_battery_deferred(self):
        self.assertFalse(allow_sync(DeviceContext(True, 10, False, False, True)))

    def test_charging_background_window(self):
        self.assertTrue(allow_sync(DeviceContext(True, 10, True, False, True)))

    def test_background_without_window(self):
        self.assertFalse(allow_sync(DeviceContext(True, 70, False, False)))

    def test_foreground_online(self):
        self.assertTrue(allow_sync(DeviceContext(True, 70, False, True)))

    def test_invalid_battery(self):
        with self.assertRaises(ValueError):
            DeviceContext(True, 101, False, True)

    def test_duplicate_delivery(self):
        inbox = Inbox()
        self.assertEqual([inbox.receive(x) for x in ("A", "B", "A")], [True, True, False])
        self.assertEqual(inbox.unique_count, 2)

    def test_blank_id_rejected(self):
        with self.assertRaises(ValueError):
            Inbox().receive("  ")

    def test_cold_model_higher_than_warm(self):
        self.assertGreater(startup_model(cold=True)["total"], startup_model(cold=False)["total"])

    def test_permission_denied(self):
        self.assertFalse(permission_decision(granted=True, user_denied=True))
        self.assertFalse(permission_decision(granted=False, user_denied=False))
        self.assertTrue(permission_decision(granted=True, user_denied=False))


if __name__ == "__main__":
    unittest.main()
