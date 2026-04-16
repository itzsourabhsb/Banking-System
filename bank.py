import sqlite3

# DATABASE SETUP
conn = sqlite3.connect("bank.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pin INTEGER NOT NULL,
    balance REAL NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    tid INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_id INTEGER,
    type TEXT,
    amount REAL
)
""")

conn.commit()


# CREATE ACCOUNT
def create_account():
    try:
        name = input("Enter name: ").strip()

        pin_input = input("Set 4-digit PIN: ").strip()
        if not pin_input.isdigit() or len(pin_input) != 4:
            print("Invalid PIN")
            return
        pin = int(pin_input)

        balance = float(input("Enter initial balance: ").strip())
        if balance < 0:
            print("Invalid balance")
            return

        cur.execute("INSERT INTO accounts (name, pin, balance) VALUES (?, ?, ?)",
                    (name, pin, balance))
        conn.commit()

        print("Account created successfully")

    except Exception as e:
        print("Error:", e)


# LOGIN
def login():
    try:
        acc_id = input("Enter Account ID: ").strip()
        pin = input("Enter PIN: ").strip()

        if not acc_id.isdigit() or not pin.isdigit():
            print("Invalid input")
            return None

        cur.execute("SELECT * FROM accounts WHERE id=? AND pin=?",
                    (int(acc_id), int(pin)))
        user = cur.fetchone()

        if user:
            print("Login successful")
            return int(acc_id)
        else:
            print("Invalid credentials")
            return None

    except Exception as e:
        print("Error:", e)
        return None


# VIEW ACCOUNTS
def view_accounts():
    data = cur.execute("SELECT id, name, balance FROM accounts")
    print("\nAccounts:")
    for row in data:
        print(row)


# DEPOSIT
def deposit():
    acc_id = login()
    if not acc_id:
        return

    try:
        amount = float(input("Enter amount: ").strip())

        if amount <= 0:
            print("Invalid amount")
            return

        cur.execute("UPDATE accounts SET balance = balance + ? WHERE id=?",
                    (amount, acc_id))

        cur.execute("INSERT INTO transactions (acc_id, type, amount) VALUES (?, ?, ?)",
                    (acc_id, "DEPOSIT", amount))

        conn.commit()
        print("Amount deposited")

    except Exception as e:
        print("Error:", e)


# WITHDRAW
def withdraw():
    acc_id = login()
    if not acc_id:
        return

    try:
        amount = float(input("Enter amount: ").strip())

        cur.execute("SELECT balance FROM accounts WHERE id=?", (acc_id,))
        result = cur.fetchone()

        if result and result[0] >= amount:
            cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?",
                        (amount, acc_id))

            cur.execute("INSERT INTO transactions (acc_id, type, amount) VALUES (?, ?, ?)",
                        (acc_id, "WITHDRAW", amount))

            conn.commit()
            print("Withdrawal successful")
        else:
            print("Insufficient balance")

    except Exception as e:
        print("Error:", e)


# TRANSACTION HISTORY
def transaction_history():
    acc_id = login()
    if not acc_id:
        return

    cur.execute("SELECT type, amount FROM transactions WHERE acc_id=?", (acc_id,))
    data = cur.fetchall()

    print("\nTransaction History:")
    for row in data:
        print(row)


# DELETE ACCOUNT
def delete_account():
    acc_id = login()
    if not acc_id:
        return

    confirm = input("Are you sure? (yes/no): ").strip()

    if confirm.lower() == "yes":
        cur.execute("DELETE FROM accounts WHERE id=?", (acc_id,))
        conn.commit()
        print("Account deleted")
    else:
        print("Cancelled")


# MAIN MENU
def main():
    while True:
        print("""
1. Create Account
2. View Accounts
3. Deposit
4. Withdraw
5. Transaction History
6. Delete Account
7. Exit
""")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            deposit()
        elif choice == "4":
            withdraw()
        elif choice == "5":
            transaction_history()
        elif choice == "6":
            delete_account()
        elif choice == "7":
            print("Thank you")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
    conn.close()
