import sqlite3
from datetime import datetime

DB_NAME = "budget.db"


def _connect(db_name):
    connection = sqlite3.connect(db_name)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def add_category(name, db_name=DB_NAME):
    connection = _connect(db_name)
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        connection.commit()
        print(f"Category added: {name}")
    except sqlite3.IntegrityError:
        print(f"Category '{name}' already exists.")
    finally:
        connection.close()


def get_all_categories(db_name=DB_NAME):
    connection = _connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()

    connection.close()
    return rows


def get_category_id(name, db_name=DB_NAME):
    connection = _connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
    row = cursor.fetchone()

    connection.close()
    return row[0] if row else None


def add_transaction(amount, description, category_name, db_name=DB_NAME):
    category_id = get_category_id(category_name, db_name=db_name)

    if category_id is None:
        print(f"Category '{category_name}' does not exist. Add it first.")
        return

    connection = _connect(db_name)
    cursor = connection.cursor()

    date = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO transactions (amount, description, date, category_id) VALUES (?, ?, ?, ?)",
        (amount, description, date, category_id)
    )

    connection.commit()
    connection.close()
    print(f"Transaction added: {description} (${amount}) under {category_name}")


def get_all_transactions(db_name=DB_NAME):
    connection = _connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT transactions.id, transactions.amount, transactions.description,
               transactions.date, categories.name
        FROM transactions
        JOIN categories ON transactions.category_id = categories.id
        ORDER BY transactions.date DESC
    """)
    rows = cursor.fetchall()

    connection.close()
    return rows


def get_transactions_by_category(category_name, db_name=DB_NAME):
    connection = _connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT transactions.id, transactions.amount, transactions.description,
               transactions.date, categories.name
        FROM transactions
        JOIN categories ON transactions.category_id = categories.id
        WHERE categories.name = ?
        ORDER BY transactions.date DESC
    """, (category_name,))
    rows = cursor.fetchall()

    connection.close()
    return rows


def get_totals_by_category(db_name=DB_NAME):
    connection = _connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT categories.name, SUM(transactions.amount)
        FROM transactions
        JOIN categories ON transactions.category_id = categories.id
        GROUP BY categories.name
    """)
    rows = cursor.fetchall()

    connection.close()
    return rows


def create_tables_for_test(db_name):
    connection = _connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)

    connection.commit()
    connection.close()