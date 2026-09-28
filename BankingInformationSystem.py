import json
from pathlib import Path

DATA_FILE = Path("accounts.json")
accounts = {}

class BankAccount:
    def __init__(self, account_number, customer_name, phone_number, balance=0.0):
        self.account_number = account_number
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.balance = float(balance)

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "customer_name": self.customer_name,
            "phone_number": self.phone_number,
            "balance": self.balance
        }

def load_accounts():
    global accounts
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            accounts = {
                x["account_number"]: BankAccount(
                    x["account_number"], x["customer_name"],
                    x["phone_number"], x["balance"]
                ) for x in data
            }
        except (json.JSONDecodeError, KeyError):
            accounts = {}

def save_accounts():
    DATA_FILE.write_text(
        json.dumps([a.to_dict() for a in accounts.values()], indent=4),
        encoding="utf-8"
    )

def next_account_number():
    nums = []
    for number in accounts:
        if number.startswith("ACC"):
            try:
                nums.append(int(number[3:]))
            except ValueError:
                pass
    return f"ACC{max(nums, default=1000) + 1:04d}"

def read_amount(prompt):
    try:
        amount = float(input(prompt))
        if amount < 0:
            print("Amount cannot be negative.")
            return None
        return amount
    except ValueError:
        print("Please enter a valid number.")
        return None

def create_account():
    print("\n--- Create Account ---")
    name = input("Enter customer name: ").strip()
    phone = input("Enter phone number: ").strip()
    if not name or not phone:
        print("Name and phone number are required.")
        return
    deposit = read_amount("Enter initial deposit: ")
    if deposit is None:
        return
    number = next_account_number()
    accounts[number] = BankAccount(number, name, phone, deposit)
    save_accounts()
    print("Account created successfully!")
    print(f"Your account number is: {number}")

def find_account():
    number = input("Enter account number: ").strip().upper()
    account = accounts.get(number)
    if account is None:
        print("Account not found.")
    return account

def deposit_money():
    print("\n--- Deposit Money ---")
    account = find_account()
    if account is None:
        return
    amount = read_amount("Enter deposit amount: ")
    if amount is None:
        return
    account.balance += amount
    save_accounts()
    print(f"Deposit successful. New balance: {account.balance:.2f}")

def withdraw_money():
    print("\n--- Withdraw Money ---")
    account = find_account()
    if account is None:
        return
    amount = read_amount("Enter withdrawal amount: ")
    if amount is None:
        return
    if amount > account.balance:
        print("Insufficient balance.")
        return
    account.balance -= amount
    save_accounts()
    print(f"Withdrawal successful. New balance: {account.balance:.2f}")

def transfer_money():
    print("\n--- Transfer Money ---")
    sender_no = input("Enter sender account number: ").strip().upper()
    receiver_no = input("Enter receiver account number: ").strip().upper()
    sender = accounts.get(sender_no)
    receiver = accounts.get(receiver_no)
    if sender is None or receiver is None:
        print("One or both accounts were not found.")
        return
    if sender_no == receiver_no:
        print("Sender and receiver must be different.")
        return
    amount = read_amount("Enter transfer amount: ")
    if amount is None:
        return
    if amount > sender.balance:
        print("Insufficient balance.")
        return
    sender.balance -= amount
    receiver.balance += amount
    save_accounts()
    print("Transfer successful!")

def check_balance():
    print("\n--- Check Balance ---")
    account = find_account()
    if account:
        print(f"Current balance: {account.balance:.2f}")

def display_account_details():
    print("\n--- Account Details ---")
    account = find_account()
    if account:
        print(f"Account Number : {account.account_number}")
        print(f"Customer Name  : {account.customer_name}")
        print(f"Phone Number   : {account.phone_number}")
        print(f"Balance        : {account.balance:.2f}")

def display_all_accounts():
    print("\n--- All Accounts ---")
    if not accounts:
        print("No accounts available.")
        return
    for a in accounts.values():
        print(f"{a.account_number} | {a.customer_name} | {a.phone_number} | Balance: {a.balance:.2f}")

def main():
    load_accounts()
    while True:
        print("\n" + "=" * 55)
        print("             BANKING INFORMATION SYSTEM")
        print("=" * 55)
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Check Balance")
        print("6. Display Account Details")
        print("7. Display All Accounts")
        print("8. Exit")
        print("-" * 40)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            create_account()
        elif choice == "2":
            deposit_money()
        elif choice == "3":
            withdraw_money()
        elif choice == "4":
            transfer_money()
        elif choice == "5":
            check_balance()
        elif choice == "6":
            display_account_details()
        elif choice == "7":
            display_all_accounts()
        elif choice == "8":
            print("Thank you for using the Banking Information System.")
            break
        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()
