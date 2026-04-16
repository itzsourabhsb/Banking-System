# Banking System (Python + SQLite)

## Overview

This project is a simple console-based banking system built using Python and SQLite.
It was created to understand how basic banking operations work along with database integration.

## What I Learned

* How to use SQLite with Python
* Creating and managing tables
* Performing CRUD operations (Create, Read, Update, Delete)
* Handling user input and validation
* Structuring code using functions

## Features

* Create account with PIN
* Login authentication
* Deposit and withdrawal operations
* Transaction history tracking
* Delete account

## Database Design

* **Accounts**: stores user details (id, name, pin, balance)
* **Transactions**: stores all deposit/withdraw records linked by account ID

## How It Works

* User creates an account with a PIN
* Login is required for sensitive operations
* Balance is updated during deposit/withdraw
* Every transaction is stored separately for history tracking

## How to Run

1. Install Python
2. Run the file:

   ```
   python bank.py
   ```

