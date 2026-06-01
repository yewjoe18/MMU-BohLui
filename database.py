import sqlite3

DB_NAME = "expense.db"


# =========================
# CREATE EXPENSE TABLE
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
        INSERT INTO expenses (
            amount,
            category,
            description
        )
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


# =========================
# CREATE STUDENT TABLE
# =========================
def create_student_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_name TEXT,

            student_email TEXT UNIQUE
        )
    """)

    conn.commit()

    conn.close()


# =========================
# REGISTER STUDENT
# =========================
def register_student(student_name, student_email):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (
            student_name,
            student_email
        )
        VALUES (?, ?)
    """, (student_name, student_email))

    conn.commit()

    conn.close()


# =========================
# LOGIN STUDENT
# =========================
def login_student(student_name, student_email):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students

        WHERE student_name = ?

        AND student_email = ?
    """, (student_name, student_email))

    student = cursor.fetchone()

    conn.close()

    return student




# =========================
# Store dates
# =========================

def insert_expense(amount, category, description, student_email, expense_date):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (
            amount,
            category,
            description,
            student_email,
            expense_date
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        amount,
        category,
        description,
        student_email,
        expense_date
    ))

    conn.commit()
    conn.close()
