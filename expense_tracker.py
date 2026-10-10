#!/usr/bin/env python3
"""Expense Tracker: a simple command-line app to record and review expenses.

Usage examples:
    python expense_tracker.py add 250 food "Lunch with friends"
    python expense_tracker.py list
    python expense_tracker.py summary
    python expense_tracker.py delete 2
    python expense_tracker.py export my_expenses.csv
"""

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    """Read all expenses from the JSON file (empty list if none yet)."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: data file is damaged. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Write all expenses to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount, category, description):
    if amount <= 0:
        print("Error: amount must be greater than 0.")
        sys.exit(1)
    expenses = load_expenses()
    expenses.append(
        {
            "date": date.today().isoformat(),
            "amount": round(amount, 2),
            "category": category.lower(),
            "description": description,
        }
    )
    save_expenses(expenses)
    print(f"Added: {amount:.2f} on {category.lower()}")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses yet. Add one with: python expense_tracker.py add 100 food")
        return
    print(f"{'#':<4}{'Date':<12}{'Category':<14}{'Amount':>10}  Description")
    print("-" * 60)
    for i, e in enumerate(expenses, start=1):
        print(
            f"{i:<4}{e['date']:<12}{e['category']:<14}{e['amount']:>10.2f}  {e['description']}"
        )


def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    grand_total = sum(totals.values())
    print(f"{'Category':<14}{'Total':>10}{'Share':>9}")
    print("-" * 33)
    for category, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"{category:<14}{total:>10.2f}{total / grand_total * 100:>8.1f}%")
    print("-" * 33)
    print(f"{'ALL':<14}{grand_total:>10.2f}")


def delete_expense(number):
    expenses = load_expenses()
    if not 1 <= number <= len(expenses):
        print(f"Error: no expense numbered {number}. Use 'list' to see numbers.")
        sys.exit(1)
    removed = expenses.pop(number - 1)
    save_expenses(expenses)
    print(f"Deleted: {removed['amount']:.2f} on {removed['category']}")


def export_csv(filename):
    expenses = load_expenses()
    if not expenses:
        print("Nothing to export yet.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["date", "amount", "category", "description"]
        )
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Exported {len(expenses)} expenses to {filename}")


def build_parser():
    parser = argparse.ArgumentParser(description="Simple command-line expense tracker.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a new expense")
    add.add_argument("amount", type=float, help="amount spent, e.g. 250")
    add.add_argument("category", help="category, e.g. food, travel, bills")
    add.add_argument("description", nargs="?", default="", help="optional note")

    sub.add_parser("list", help="show all expenses")
    sub.add_parser("summary", help="show totals by category")

    delete = sub.add_parser("delete", help="delete an expense by its number")
    delete.add_argument("number", type=int, help="number shown by 'list'")

    export = sub.add_parser("export", help="export expenses to a CSV file")
    export.add_argument("filename", nargs="?", default="expenses.csv")

    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "add":
        add_expense(args.amount, args.category, args.description)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary()
    elif args.command == "delete":
        delete_expense(args.number)
    elif args.command == "export":
        export_csv(args.filename)


if __name__ == "__main__":
    main()
