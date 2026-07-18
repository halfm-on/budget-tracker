import argparse
from database import (
    add_category,
    get_all_categories,
    add_transaction,
    get_all_transactions,
    get_transactions_by_category,
    get_totals_by_category,
)


def view_transactions(category=None):
    transactions = get_transactions_by_category(category) if category else get_all_transactions()

    if not transactions:
        print("No transactions found.")
        return

    for t_id, amount, description, date, category_name in transactions:
        print(f"[{t_id}] {date} | {category_name}: {description} — ${amount:.2f}")


def view_categories():
    categories = get_all_categories()

    if not categories:
        print("No categories found.")
        return

    for cat_id, name in categories:
        print(f"[{cat_id}] {name}")


def view_totals():
    totals = get_totals_by_category()

    if not totals:
        print("No spending recorded yet.")
        return

    for category_name, total in totals:
        print(f"{category_name}: ${total:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Track budget categories and transactions.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cat_parser = subparsers.add_parser("add-category", help="Add a new category")
    cat_parser.add_argument("name", help="Category name, e.g. Groceries")

    tx_parser = subparsers.add_parser("add-transaction", help="Add a transaction")
    tx_parser.add_argument("amount", type=float, help="Transaction amount, e.g. 45.50")
    tx_parser.add_argument("description", help="Short description, e.g. 'Weekly shop'")
    tx_parser.add_argument("category", help="Category name, must already exist")

    view_parser = subparsers.add_parser("view", help="View transactions")
    view_parser.add_argument("--category", help="Filter by category name", default=None)

    subparsers.add_parser("categories", help="View all categories")
    subparsers.add_parser("totals", help="View spending totals by category")

    args = parser.parse_args()

    if args.command == "add-category":
        add_category(args.name)
    elif args.command == "add-transaction":
        add_transaction(args.amount, args.description, args.category)
    elif args.command == "view":
        view_transactions(args.category)
    elif args.command == "categories":
        view_categories()
    elif args.command == "totals":
        view_totals()


if __name__ == "__main__":
    main()