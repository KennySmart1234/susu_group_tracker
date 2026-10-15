from decimal import Decimal
from susu import SusuGroup

group = SusuGroup("50.00")

group.add_member("Ama")
group.add_member("Kofi")
group.add_member("Esi")

print("Weekly contribution:", group.weekly_contribution)
print("Members:", group.get_members())
print("Current week:", group.current_week)

assert group.weekly_contribution == Decimal("50.00")
assert group.get_members() == ["Ama", "Kofi", "Esi"]
assert group.current_week == 1

print("Basic checks passed!")
