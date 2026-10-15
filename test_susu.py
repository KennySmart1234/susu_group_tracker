
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




if __name__ == "__main__":
    unittest.main()
