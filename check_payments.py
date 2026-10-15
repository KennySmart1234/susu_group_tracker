from decimal import Decimal
from susu import SusuGroup

group = SusuGroup("50.00")
group.add_member("Ama")
group.add_member("Kofi")
group.add_member("Esi")

# Two members pay in full; Esi makes a partial payment.
group.record_contribution("Ama", "50.00")
group.record_contribution("Kofi", "50.00")
group.record_contribution("Esi", "30.00")

# The week must remain open.
result = group.close_week()

assert result["closed"] is False
assert result["unpaid"]["Esi"] == Decimal("20.00")
assert group.current_week == 1
assert len(group.payout_history) == 0

# Esi pays the outstanding balance.
group.record_contribution("Esi", "20.00")
result = group.close_week()

assert result["closed"] is True
assert result["payout"]["recipient"] == "Ama"
assert result["payout"]["amount"] == Decimal("150.00")
assert group.current_week == 2

print("All payment and payout checks passed!")
