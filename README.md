# Susu Group Tracker

## Project Overview

Susu Group Tracker is a Python command-line application that manages a
rotating savings group. Members contribute a fixed amount each week,
and one member receives the collected pot after everyone has paid.

## Features

- Create a group with a fixed weekly contribution in Ghanaian cedis (GHS).
- Add unique members.
- Record full or partial contributions.
- Calculate outstanding balances.
- Reject unknown members, zero payments, and payments above the
  outstanding balance.
- Prevent a week from closing when members still owe money.
- Rotate payouts among group members.
- View weekly payment reports and payout history.

## Requirements

- Python 3.10 or newer recommended.
- No external Python packages required.

## Installation

Clone the repository:

    git clone https://github.com/KennySmart1234/susu_group_tracker.git
    cd susu_group_tracker

Optionally create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

## Run the Application

    python3 main.py

Follow the menu to add members, record contributions, check balances,
close weeks, and view reports.

## Run the Automated Tests

    python3 -m unittest -v

## Project Files

- `susu.py` - Core group, contribution, and payout logic.
- `main.py` - Interactive command-line interface.
- `test_susu.py` - Automated unit tests.
- `NOTES.md` - Assumptions, limitations, and possible improvements.

## Limitations

Data is stored in memory and is lost when the program exits.
The application does not make real bank transfers.
