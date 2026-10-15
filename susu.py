
from decimal import Decimal, InvalidOperation


class SusuGroup:
    """Manage the basic details of a rotating savings group."""

    def __init__(self, weekly_contribution):
        self.weekly_contribution = self._to_money(
            weekly_contribution
        )

        if self.weekly_contribution <= Decimal("0.00"):
            raise ValueError(
                "Weekly contribution must be greater than zero."
            )

        self.members = []
        self.current_week = 1
        self.contributions = {}
        self.payout_history = []

    @staticmethod
    def _to_money(amount):
        """Convert an amount to Decimal without using float arithmetic."""
        try:
            money = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Amount must be a valid number.") from None

        if not money.is_finite():
            raise ValueError("Amount must be a finite number.")

        if money.as_tuple().exponent < -2:
            raise ValueError(
                "Money must have no more than two decimal places."
            )

        return money.quantize(Decimal("0.01"))

    def add_member(self, name):
        """Add a member if the name is valid and unique."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Member name cannot be empty.")

        name = name.strip()

        if any(
            member.casefold() == name.casefold()
            for member in self.members
        ):
            raise ValueError("This member already exists.")

        if self.contributions:
            raise ValueError(
                "Cannot add members after contributions have started."
            )

        self.members.append(name)

    def get_members(self):
        """Return a copy of the member list."""
        return self.members.copy()
