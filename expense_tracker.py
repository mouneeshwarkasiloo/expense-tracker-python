# expense tracker.
# Maintains expenses in a JSON file and lets the user add, view, and summarize
# the entries in a minimal text-menu interface.

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict


# Location where all data will be stored.
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "expenses.json"


@dataclass
class Expense:
    id: int
    date: str          # format: YYYY-MM-DD
    category: str
    description: str
    amount: float

def load_expenses() -> List[Expense]:
    """Read existing expenses from disk. If the file does not exist, return empty."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Corrupted or empty file → start fresh
        return []
    result: List[Expense] = []
    for item in raw:
        result.append(
            Expense(
                id=item.get("id"),
                date=item.get("date"),
                category=item.get("category"),
                description=item.get("description"),
                amount=float(item.get("amount", 0)),
            )
        )
    return result


def save_expenses(items: List[Expense]) -> None:
    """Write the current list of expenses to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in items], f, indent=2)


def next_id(expenses: List[Expense]) -> int:
    """Find the next available ID."""
    if not expenses:
        return 1
    return max(e.id for e in expenses) + 1


def add_expense(expenses: List[Expense]) -> None:
    print("\n--- Add Expense ---")

    today = datetime.today().strftime("%Y-%m-%d")
    date_in = input(f"Date (YYYY-MM-DD) [default {today}]: ").strip()
    if date_in == "":
        date_in = today

    cat = input("Category (food/travel/etc): ").strip()
    if not cat:
        cat = "uncategorized"

    desc = input("Description: ").strip()
    if not desc:
        desc = "No description"

    while True:
        amt_raw = input("Amount: ").strip()
        try:
            amt = float(amt_raw)
            if amt < 0:
                print("Amount cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
            continue

    new = Expense(
        id=next_id(expenses),
        date=date_in,
        category=cat,
        description=desc,
        amount=amt
    )

    expenses.append(new)
    save_expenses(expenses)
    print(f"Added expense #{new.id}.\n")


def list_expenses(expenses: List[Expense]) -> None:
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses yet.\n")
        return

    print(f"{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':>10}  Description")
    print("-" * 60)

    for e in expenses:
        print(f"{e.id:<4} {e.date:<12} {e.category:<15} {e.amount:>10.2f}  {e.description}")

    total = sum(e.amount for e in expenses)
    print("-" * 60)
    print(f"{'':<4} {'':<12} {'TOTAL':<15} {total:>10.2f}\n")


def summary_by_category(expenses: List[Expense]) -> None:
    print("\n--- Summary by Category ---")

    if not expenses:
        print("No expenses yet.\n")
        return

    totals: Dict[str, float] = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category, 0) + e.amount

    print(f"{'Category':<20} {'Total':>12}")
    print("-" * 32)
    for cat, amt in sorted(totals.items()):
        print(f"{cat:<20} {amt:>12.2f}")
    print()


def summary_by_month(expenses: List[Expense]) -> None:
    print("\n--- Summary by Month ---")

    if not expenses:
        print("No expenses yet.\n")
        return

    monthly: Dict[str, float] = {}
    for e in expenses:
        month = e.date[:7]   # YYYY-MM
        monthly[month] = monthly.get(month, 0) + e.amount

    print(f"{'Month':<10} {'Total':>12}")
    print("-" * 24)
    for m, amt in sorted(monthly.items()):
        print(f"{m:<10} {amt:>12.2f}")
    print()


def main_menu():
    expenses = load_expenses()

    menu = """
=============================
     Expense Tracker
=============================
 1. Add expense
 2. List all expenses
 3. Summary by category
 4. Summary by month
 5. Exit
"""

    while True:
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            summary_by_category(expenses)
        elif choice == "4":
            summary_by_month(expenses)
        elif choice == "5":
            print("Exiting…")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main_menu()
