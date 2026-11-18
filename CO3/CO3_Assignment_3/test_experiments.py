import unittest
from experiments import choose_access_point, shortest_hop_path, update_home_binding, sample_trace


class CO3Tests(unittest.TestCase):
    def test_no_ping_pong_near_margin(self):
        self.assertEqual(choose_access_point("AP1", {"AP1": -60, "AP2": -58}), "AP1")

    def test_handoff_on_stronger_signal(self):
        self.assertEqual(choose_access_point("AP1", {"AP1": -78, "AP2": -59}), "AP2")

    def test_handoff_trace(self):
        self.assertEqual(sample_trace()[-1]["selected_ap"], "AP2")

    def test_connected_path(self):
        self.assertEqual(shortest_hop_path({"A":["B"],"B":["C"],"C":[]}, "A", "C"), ["A","B","C"])

    def test_unreachable(self):
        self.assertIsNone(shortest_hop_path({"A": [], "B": []}, "A", "B"))

    def test_stale_binding(self):
        table = {}
        self.assertTrue(update_home_binding(table, "home", "coa1", 2))
        self.assertFalse(update_home_binding(table, "home", "coa2", 1))
        self.assertEqual(table["home"][0], "coa1")


if __name__ == "__main__":
    unittest.main()
