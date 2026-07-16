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