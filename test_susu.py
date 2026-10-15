
import unittest
from decimal import Decimal

from susu import SusuGroup


class TestSusuGroup(unittest.TestCase):

    def setUp(self):
        self.group = SusuGroup("50.00")
        self.group.add_member("Ama")
        self.group.add_member("Kofi")
        self.group.add_member("Esi")

    def test_group_creation(self):
        self.assertEqual(
            self.group.weekly_contribution,
            Decimal("50.00"),
        )

    def test_add_member(self):
        self.group.add_member("Yaw")
        self.assertIn("Yaw", self.group.get_members())

    def test_reject_duplicate_member(self):
        with self.assertRaises(ValueError):
            self.group.add_member("ama")

    def test_partial_payment(self):
        self.group.record_contribution("Esi", "30.00")

        self.assertEqual(
            self.group.outstanding_balance("Esi"),
            Decimal("20.00"),
        )

    def test_week_cannot_close_with_unpaid_balance(self):
        self.group.record_contribution("Ama", "50.00")
        self.group.record_contribution("Kofi", "50.00")
        self.group.record_contribution("Esi", "30.00")

        result = self.group.close_week()

        self.assertFalse(result["closed"])
        self.assertEqual(
            result["unpaid"]["Esi"],
            Decimal("20.00"),
        )
        self.assertEqual(self.group.current_week, 1)
        self.assertEqual(len(self.group.payout_history), 0)

    def test_successful_payout(self):
        for member in self.group.get_members():
            self.group.record_contribution(member, "50.00")

        result = self.group.close_week()

        self.assertTrue(result["closed"])
        self.assertEqual(result["payout"]["recipient"], "Ama")
        self.assertEqual(
            result["payout"]["amount"],
            Decimal("150.00"),
        )
        self.assertEqual(self.group.current_week, 2)

    def test_reject_payment_above_balance(self):
        with self.assertRaises(ValueError):
            self.group.record_contribution("Ama", "50.01")

    def test_reject_zero_payment(self):
        with self.assertRaises(ValueError):
            self.group.record_contribution("Ama", "0.00")

    def test_reject_unknown_member(self):
        with self.assertRaises(ValueError):
            self.group.record_contribution("Unknown", "10.00")


if __name__ == "__main__":
    unittest.main()
