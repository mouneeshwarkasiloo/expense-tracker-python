"""
A small command-line tool for tracking personal expenses.
Data is stored inside a JSON file (data/expenses.json). The idea
is to keep it simple but still useful enough for daily usage.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict


# Data file setup
ROOT_DIR = Path(__file__).parent
DATA_FOLDER = ROOT_DIR / "data"
EXPENSE_FILE = DATA_FOLDER / "expenses.json"


@dataclass
class Expense:
    """Represents a single expense entry."""
    id: int
    date: str
    category: str
    description: str
    amount: float


def load_expenses() -> List[Expense]:
    """Reads all saved expenses from the JSON file."""
    if not EXPENSE_FILE.exists():
        return []

    try:
        raw = json.loads(EXPENSE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    items: List[Expense] = []
    for entry in raw:
        items.append(
            Expense(
                id=entry.get("id", 0),
                date=entry.get("date", ""),
                category=entry.get("category", ""),
                description=entry.get("description", ""),
                amount=float(entry.get("amount", 0)),
            )
        )
    return items


def save_expenses(expenses: List[Expense]) -> None:
    """Writes the full expense list back to the JSON file."""
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    EXPENSE_FILE.write_text(
        json.dumps([asdict(e) for e in expenses], indent=2),
        encoding="utf-8",
    )


def next_id(expenses: List[Expense]) -> int:
    """Returns the next ID (auto-increment style)."""
    if not expenses:
        return 1
    return max(e.id for e in expenses) + 1


def add_expense(expenses: List[Expense]) -> None:
    """Lets the user add an expense interactively."""
    print("\n--- Add Expense ---")

    today = datetime.today().strftime("%Y-%m-%d")
    raw_date = input(f"Date (YYYY-MM-DD) [default: {today}]: ").strip()
    if not raw_date:
        raw_date = today

    category = input("Category: ").strip() or "uncategorized"
    desc = input("Description: ").strip() or "No description"

    # amount validation
    while True:
        amount_input = input("Amount: ").strip()
        try:
            money = float(amount_input)
            if money < 0:
                print("Amount cannot be negative.")
                continue
            break
        except ValueError:
            print("Enter a valid number (example: 99.50)")

    new_entry = Expense(
        id=next_id(expenses),
        date=raw_date,
        category=category,
        description=desc,
        amount=money,
    )

    expenses.append(new_entry)
    save_expenses(expenses)

    print(f"Added expense #{new_entry.id} successfully.\n")


def list_expenses(expenses: List[Expense]) -> None:
    """Displays all expenses in a simple table."""
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded.\n")
        return

    print(f"{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':>10}  Description")
    print("-" * 62)

    for e in expenses:
        print(f"{e.id:<4} {e.date:<12} {e.category:<15} {e.amount:>10.2f}  {e.description}")

    total = sum(e.amount for e in expenses)
    print("-" * 62)
    print(f"{'':<4} {'':<12} {'TOTAL':<15} {total:>10.2f}\n")


def summary_category(expenses: List[Expense]) -> None:
    """Prints total spent for each category."""
    print("\n--- Category Summary ---")

    if not expenses:
        print("No expenses recorded.\n")
        return

    totals: Dict[str, float] = {}

    for e in expenses:
        totals[e.category] = totals.get(e.category, 0) + e.amount

    print(f"{'Category':<20} {'Total Spent':>15}")
    print("-" * 38)

    for cat, amt in sorted(totals.items()):
        print(f"{cat:<20} {amt:>15.2f}")

    print()


def summary_month(expenses: List[Expense]) -> None:
    """Shows monthly spending breakdown."""
    print("\n--- Monthly Summary ---")

    if not expenses:
        print("No expenses recorded.\n")
        return

    monthly: Dict[str, float] = {}
    for e in expenses:
        month = e.date[:7]  # YYYY-MM
        monthly[month] = monthly.get(month, 0) + e.amount

    print(f"{'Month':<10} {'Total Spent':>15}")
    print("-" * 28)
    
    for m, total in sorted(monthly.items()):
        print(f"{m:<10} {total:>15.2f}")
    print()
def reset_expenses() -> None:
    """Deletes all stored expenses."""
    confirm = input(
        "\nAre you sure you want to clear ALL expenses? This cannot be undone. (yes/no): "
    ).strip().lower()
    if confirm in ("yes", "y"):
        DATA_FOLDER.mkdir(parents=True, exist_ok=True)
        EXPENSE_FILE.write_text("[]", encoding="utf-8")
        print("All expense records cleared.\n")
    else:
        print("Reset cancelled.\n")
def menu():
    expenses = load_expenses()

    while True:
        print("""
============================
      Expense Tracker
============================
1. Add Expense
2. List Expenses
3. Summary by Category
4. Summary by Month
5. Reset All Records
6. Exit
""")
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            summary_category(expenses)
        elif choice == "4":
            summary_month(expenses)
        elif choice == "5":
            reset_expenses()
            expenses = load_expenses()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.\n")
if __name__ == "__main__":
    menu()
