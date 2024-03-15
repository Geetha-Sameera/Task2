import json
from datetime import datetime


class Transaction:
    def __init__(self, category, amount, transaction_type):
        self.category = category
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class BudgetTracker:
    def __init__(self, transactions_file):
        self.transactions_file = transactions_file
        self.transactions = self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.transactions_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_transactions(self):
        with open(self.transactions_file, 'w') as file:
            json.dump(self.transactions, file, default=lambda o: o.__dict__, indent=4)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self, income):
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return income - expenses

    def display_expense_analysis(self):
        categories = {}
        for transaction in self.transactions:
            if transaction.transaction_type == 'expense':
                categories[transaction.category] = categories.get(transaction.category, 0) + transaction.amount
        for category, amount in categories.items():
            print(f"{category}: ${amount}")

    def list_transactions(self):
        for transaction in self.transactions:
            print(f"{transaction.category} - Amount: ${transaction.amount}, Type: {transaction.transaction_type}, Date: {transaction.date}")


if __name__ == "__main__":
    budget_tracker = BudgetTracker('transactions.json')

    while True:
        print("\nBudget Tracker Application")
        print("1. Add Transaction")
        print("2. Calculate Budget")
        print("3. Display Expense Analysis")
        print("4. List Transactions")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            category = input("Enter transaction category: ")
            amount = float(input("Enter amount: "))
            transaction_type = input("Enter transaction type (income/expense): ")
            budget_tracker.add_transaction(Transaction(category, amount, transaction_type))
        elif choice == '2':
            income = float(input("Enter total income: "))
            remaining_budget = budget_tracker.calculate_budget(income)
            print(f"Remaining Budget: ${remaining_budget}")
        elif choice == '3':
            budget_tracker.display_expense_analysis()
        elif choice == '4':
            budget_tracker.list_transactions()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
