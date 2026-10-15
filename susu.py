
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



    def record_contribution(self, member_name, amount):
        """Record a full or partial payment for the current week."""
        if member_name not in self.members:
            raise ValueError("Unknown member.")

        payment = self._to_money(amount)

        if payment <= Decimal("0.00"):
            raise ValueError("Payment must be greater than zero.")

        week_payments = self.contributions.setdefault(
            self.current_week, {}
        )

        already_paid = week_payments.get(
            member_name, Decimal("0.00")
        )

        outstanding = self.weekly_contribution - already_paid

        if payment > outstanding:
            raise ValueError(
                f"Payment exceeds the outstanding balance of "
                f"{outstanding:.2f}."
            )

        week_payments[member_name] = already_paid + payment

    def outstanding_balance(self, member_name):
        """Return how much a member still owes this week."""
        if member_name not in self.members:
            raise ValueError("Unknown member.")

        paid = self.contributions.get(
            self.current_week, {}
        ).get(member_name, Decimal("0.00"))

        return self.weekly_contribution - paid

    def close_week(self):
        """Close the current week if every member has paid in full."""
        if not self.members:
            raise ValueError("Cannot close a group with no members.")

        unpaid = {
            member: self.outstanding_balance(member)
            for member in self.members
            if self.outstanding_balance(member) > Decimal("0.00")
        }

        if unpaid:
            return {
                "closed": False,
                "week": self.current_week,
                "unpaid": unpaid,
            }

        payout_index = len(self.payout_history) % len(self.members)
        recipient = self.members[payout_index]

        pot = self.weekly_contribution * len(self.members)

        payout = {
            "week": self.current_week,
            "recipient": recipient,
            "amount": pot,
        }

        self.payout_history.append(payout)
        self.current_week += 1

        return {
            "closed": True,
            "payout": payout,
        }

    def get_report(self):
        """Return a report for the current week and payout history."""
        week_payments = self.contributions.get(
            self.current_week, {}
        )

        members_report = {}

        for member in self.members:
            paid = week_payments.get(
                member, Decimal("0.00")
            )

            members_report[member] = {
                "paid": paid,
                "owes": self.weekly_contribution - paid,
                "paid_in_full": paid == self.weekly_contribution,
            }

        return {
            "current_week": self.current_week,
            "members": members_report,
            "payout_history": self.payout_history.copy(),
        }
