import csv
import os
from datetime import datetime

import pandas as pd

FILE_NAME = "transactions.csv"


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Category", "Amount"])


def add_transaction(transaction_type):
    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty!")
        return

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid amount!")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, transaction_type, category, amount])

    print(f"{transaction_type} added successfully!")


def view_transactions():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        transactions = list(reader)

    if len(transactions) <= 1:
        print("No transactions found!")
        return

    print("\n========== ALL TRANSACTIONS ==========")

    for row in transactions:
        print(" | ".join(row))


def financial_summary():
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        transactions = list(reader)

    total_income = 0
    total_expense = 0

    current_month = datetime.now().strftime("%Y-%m")

    monthly_income = 0
    monthly_expense = 0

    for transaction in transactions:
        amount = float(transaction["Amount"])

        if transaction["Type"] == "Income":
            total_income += amount

            if transaction["Date"].startswith(current_month):
                monthly_income += amount

        elif transaction["Type"] == "Expense":
            total_expense += amount

            if transaction["Date"].startswith(current_month):
                monthly_expense += amount

    balance = total_income - total_expense

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Income: ₹{total_income:.2f}")
    print(f"Total Expenses: ₹{total_expense:.2f}")
    print(f"Current Balance: ₹{balance:.2f}")

    print("\n========== THIS MONTH ==========")
    print(f"Monthly Income: ₹{monthly_income:.2f}")
    print(f"Monthly Expenses: ₹{monthly_expense:.2f}")


def filter_transactions():
    print("\n1. Filter by Date")
    print("2. Filter by Category")

    choice = input("Enter your choice: ")

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        transactions = list(reader)

    if choice == "1":
        search_value = input("Enter date (YYYY-MM-DD): ").strip()
        filtered = [
            t for t in transactions
            if t["Date"] == search_value
        ]

    elif choice == "2":
        search_value = input("Enter category: ").strip().lower()
        filtered = [
            t for t in transactions
            if t["Category"].lower() == search_value
        ]

    else:
        print("Invalid choice!")
        return

    if not filtered:
        print("No matching transactions found!")
        return

    print("\n========== FILTERED TRANSACTIONS ==========")

    for transaction in filtered:
        print(
            f'{transaction["Date"]} | '
            f'{transaction["Type"]} | '
            f'{transaction["Category"]} | '
            f'₹{float(transaction["Amount"]):.2f}'
        )


def export_to_excel():
    try:
        if not os.path.exists(FILE_NAME):
            print("No transaction file found!")
            return

        df = pd.read_csv(FILE_NAME)

        if df.empty:
            print("No transactions available to export!")
            return

        output_file = "expense_report.xlsx"
        df.to_excel(output_file, index=False)

        print(f"Excel report exported successfully: {output_file}")

    except Exception as error:
        print(f"Export failed: {error}")


def main():
    initialize_file()

    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Financial Summary")
        print("5. Filter Transactions")
        print("6. Export to Excel")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_transaction("Income")

        elif choice == "2":
            add_transaction("Expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            financial_summary()

        elif choice == "5":
            filter_transactions()

        elif choice == "6":
            export_to_excel()

        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()