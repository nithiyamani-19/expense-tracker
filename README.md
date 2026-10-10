# Expense Tracker

A simple command-line expense tracker written in Python. Record what you spend, see where your money goes, and export everything to CSV. No external libraries needed.

## Features

- Add expenses with an amount, category and optional note
- List all expenses with numbering
- Summary of totals and percentage share by category
- Delete expenses by number
- Export to a CSV file (opens in Excel or Google Sheets)
- Data saved locally in `expenses.json`

## Requirements

- Python 3.8 or newer

## Usage

```bash
# Add expenses
python expense_tracker.py add 250 food "Lunch with friends"
python expense_tracker.py add 1200 travel "Train ticket"

# See everything
python expense_tracker.py list

# Totals by category
python expense_tracker.py summary

# Delete expense number 2
python expense_tracker.py delete 2

# Export to CSV
python expense_tracker.py export my_expenses.csv
```

### Example output

```
Category         Total    Share
---------------------------------
travel         1200.00    82.8%
food            250.00    17.2%
---------------------------------
ALL            1450.00
```

## Project structure

```
expense-tracker/
├── expense_tracker.py   # the whole app
├── README.md
├── LICENSE
└── .gitignore
```

## Ideas for future improvements

- Filter by date range or month
- Monthly budgets with warnings
- Charts using matplotlib
- Edit an existing expense

## License

MIT License. See [LICENSE](LICENSE).
