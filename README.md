# FinSight CLI (Evolution of Expense Tracker)

## Overview

This repository represents the evolution of a command-line based personal finance tool, developed progressively as my understanding of programming concepts improved.

The project began as a simple expense tracker built using Python and JSON storage, and was later redesigned into a more structured and insight-driven system using SQLite and terminal-based visualizations.

---

## Version History

### Version 1 — Expense Tracker (JSON-based)

The initial version of this project was developed when I had a foundational understanding of Python but no exposure to databases.

Key characteristics:

* Data stored locally using JSON files
* Basic CLI interaction
* Expense recording and simple summaries
* No structured data management

This version helped me understand:

* Input handling
* File operations
* Basic program structure

File:

```
V1_Expense_Tracker.py
```

---

### Version 2 — FinSight CLI (SQLite + Insights)

After learning SQL and gaining more experience with structured programming, I revisited the project and redesigned it into a more robust system.

Key improvements:

* Migration from JSON to SQLite database
* Structured data storage with tables
* Income and savings goal tracking
* Financial insights (balance, safe spending, savings evaluation)
* CLI-based visual graphs using ASCII representation
* Improved input validation and cleaner flow

This version reflects:

* Better system design thinking
* Use of databases instead of flat files
* Focus on user insights, not just data storage

File:

```
V2_FinSight.py
```

---

## Features (Current Version)

* Track daily expenses
* Store data using SQLite
* Set income and savings targets
* View financial insights:

  * Total spending
  * Remaining balance
  * Safe-to-spend amount
* Category-wise expense breakdown
* CLI-based bar graph visualization

---

## Tech Stack

* Python
* SQLite
* Command Line Interface (ANSI styling)

---

## How to Run

```bash
python3 V2_FinSight.py
```

---

## Why This Project Matters

This project demonstrates progression from a basic script to a more structured application.

It reflects:

* Learning-by-building approach
* Iterative improvement
* Transition from simple storage (JSON) to relational databases (SQLite)
* Focus on usability and insights

---

