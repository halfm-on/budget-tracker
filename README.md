# Budget Tracker

A command-line tool to track expenses using a local SQLite database, with categories and transactions linked through a relational structure.

## Features

- Create spending categories (e.g. Groceries, Rent, Entertainment)
- Log transactions linked to a category
- View all transactions with their category name
- View transactions filtered by category
- View total spending per category
- Prevents duplicate categories and invalid category references

## Project Structure
budget-tracker/
├── project.py          # CLI entry point
├── database.py          # All SQLite operations
├── db_setup.py            # Creates the categories and transactions tables
├── test_database.py        # Unit tests
├── requirements.txt
└── README.md

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/halfm-on/budget-tracker.git
   cd budget-tracker
```

2. Create the database:
```bash
   python3 db_setup.py
```

## Database Design

The project uses two related tables:

- **categories** — id, name
- **transactions** — id, amount, description, date, category_id (foreign key referencing categories)

Each transaction must belong to an existing category, enforced through SQLite foreign key constraints.

## What I Learned

This project was built to practice relational database design in SQLite, including:
- Foreign key relationships between tables
- Using `JOIN` to combine data across tables
- Using `GROUP BY` and `SUM` for aggregate reporting
- Handling constraint violations (like duplicate categories) with exceptions

## License

This project is open source and available under the MIT License.

## Usage

### Add a category

```bash
python3 project.py add-category Groceries
```

### Add a transaction

```bash
python3 project.py add-transaction 45.50 "Weekly shop" Groceries
```

### View all transactions

```bash
python3 project.py view
```

### View transactions for a category

```bash
python3 project.py view --category Groceries
```

### View all categories

```bash
python3 project.py categories
```

### View spending totals by category

```bash
python3 project.py totals
```

## Running Tests

```bash
python3 -m pytest -v
```