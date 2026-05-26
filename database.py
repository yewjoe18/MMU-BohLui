import sqlite3

DB_NAME = "expense.db"

# =========================
# CREATE DATABASE TABLE
# =========================
def create_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# INSERT EXPENSE
# =========================
def insert_expense(amount, category, description):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, description)
        VALUES (?, ?, ?)
    """, (amount, category, description))

    conn.commit()
    conn.close()


# =========================
# GET ALL EXPENSES
# =========================
def get_expenses():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    data = cursor.fetchall()

    conn.close()

    return data


# =========================
# DELETE EXPENSE
# =========================
def delete_expense(expense_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()