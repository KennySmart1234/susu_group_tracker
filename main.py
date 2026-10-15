from decimal import Decimal
from susu import SusuGroup


def show_report(group):
    report = group.get_report()

    print(f"\n--- Week {report['current_week']} Report ---")
    print(f"Weekly contribution: GHS {group.weekly_contribution:.2f}")

    if not report["members"]:
        print("No members have been added yet.")

    for name, details in report["members"].items():
        status = (
            "Paid in full"
            if details["paid_in_full"]
            else "Payment outstanding"
        )

        print(f"\nMember: {name}")
        print(f"  Paid: GHS {details['paid']:.2f}")
        print(f"  Owes: GHS {details['owes']:.2f}")
        print(f"  Status: {status}")

    print("\n--- Payout History ---")

    if not report["payout_history"]:
        print("No payouts have been made yet.")
    else:
        for payout in report["payout_history"]:
            print(
                f"Week {payout['week']}: "
                f"{payout['recipient']} received "
                f"GHS {payout['amount']:.2f}"
            )


def main():
    print("=" * 40)
    print("       SUSU GROUP TRACKER")
    print("=" * 40)

    while True:
        try:
            amount = input(
                "Enter the weekly contribution in GHS: "
            ).strip()

            group = SusuGroup(amount)
            break
        except ValueError as error:
            print(f"Error: {error}. Please try again.")

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Add member")
        print("2. View members")
        print("3. Record contribution")
        print("4. Check outstanding balance")
        print("5. Close week and make payout")
        print("6. View report")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        try:
            if choice == "1":
                name = input("Enter member name: ")
                group.add_member(name)
                print(f"{name.strip()} added successfully.")

            elif choice == "2":
                members = group.get_members()

                if not members:
                    print("No members have been added yet.")
                else:
                    print("\nGroup Members:")
                    for number, name in enumerate(members, start=1):
                        print(f"{number}. {name}")

            elif choice == "3":
                name = input("Enter member name: ").strip()
                amount = input("Enter payment amount in GHS: ").strip()

                group.record_contribution(name, amount)

                print(
                    f"Payment recorded. "
                    f"Outstanding balance: "
                    f"GHS {group.outstanding_balance(name):.2f}"
                )

            elif choice == "4":
                name = input("Enter member name: ").strip()
                balance = group.outstanding_balance(name)

                print(
                    f"{name} owes GHS {balance:.2f} "
                    f"for week {group.current_week}."
                )

            elif choice == "5":
                result = group.close_week()

                if not result["closed"]:
                    print(
                        f"Week {result['week']} cannot close. "
                        "The following members still owe money:"
                    )

                    for name, balance in result["unpaid"].items():
                        print(f"- {name}: GHS {balance:.2f}")
                else:
                    payout = result["payout"]

                    print(f"Week {payout['week']} closed successfully.")
                    print(f"Recipient: {payout['recipient']}")
                    print(f"Payout: GHS {payout['amount']:.2f}")

            elif choice == "6":
                show_report(group)

            elif choice == "7":
                print("Thank you for using Susu Group Tracker.")
                break

            else:
                print("Invalid option. Please choose from 1 to 7.")

        except ValueError as error:
            print(f"Error: {error}")

        except (EOFError, KeyboardInterrupt):
            print("\nExiting Susu Group Tracker.")
            break


if __name__ == "__main__":
    main()
