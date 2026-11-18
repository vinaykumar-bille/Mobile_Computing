import unittest
from experiments import Work, Environment, decide, rank_items, choose_media_kbps


class CO5Tests(unittest.TestCase):
    def test_permission_refusal(self):
        self.assertEqual(decide(Work("a", False, True, True), Environment(True, 100)), "REJECT_PERMISSION")

    def test_plaintext_refusal_even_if_critical(self):
        self.assertEqual(decide(Work("a", True, False, True, True), Environment(True, 100)), "REJECT_ENCRYPTION")

    def test_offline_deferral(self):
        self.assertEqual(decide(Work("a", True, True, True), Environment(False, 80)), "DEFER_OFFLINE")

    def test_low_battery(self):
        self.assertEqual(decide(Work("a", True, True, True), Environment(True, 10)), "DEFER_BATTERY")

    def test_charging(self):
        self.assertEqual(decide(Work("a", True, True, True), Environment(True, 10, True)), "SCHEDULE")

    def test_approximate_reduces_scan(self):
        items = [("a", 0.1), ("b", 0.8), ("c", 0.4)]
        self.assertEqual(rank_items(items)[1], 3)
        self.assertEqual(rank_items(items, 2)[1], 2)

    def test_bitrate(self):
        self.assertEqual(choose_media_kbps(300), 240)
        self.assertEqual(choose_media_kbps(5000), 1800)


if __name__ == "__main__":
    unittest.main()
