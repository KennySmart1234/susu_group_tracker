# Development Notes

## Assumptions

1. Each Susu group has a fixed weekly contribution amount.
2. Money amounts must be positive and have no more than two decimal
   places.
3. Each member must have a unique name, ignoring letter case.
4. Members cannot be added after contributions have started.
5. Partial payments are allowed.
6. A week can close only when every member has paid the full weekly
   contribution.
7. The payout goes to one member at a time, in the order members were
   added.
8. After every member has received a payout, the rotation starts again
   with the first member.
9. The payout amount equals the weekly contribution multiplied by the
   number of members.

## Current Limitations

- Group data is stored in memory and is lost when the program exits.
- Member names are used as identifiers rather than unique member IDs.
- The program manages one group per session.
- There is no database or graphical user interface.
- The application records payouts but does not transfer real money.
- Contributions and payout records are not timestamped.

## Possible Improvements

- Add database storage so data persists between sessions.
- Support multiple groups.
- Give every member a unique ID.
- Add timestamps to payments and payouts.
- Export reports to CSV.
- Expand tests to cover invalid amounts, empty groups, and payout
  rotation across multiple weeks.
- Add authentication and authorization before supporting real financial
  information.
