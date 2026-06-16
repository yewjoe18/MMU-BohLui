import sqlite3

DB_NAME = "expense.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            description TEXT,
            student_email TEXT,
            expense_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_expense(amount, category, description, student_email, expense_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, description, student_email, expense_date)
        VALUES (?, ?, ?, ?, ?)
    """, (amount, category, description, student_email, expense_date))
    conn.commit()
    conn.close()

def get_expenses(current_email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE student_email = ?", (current_email,))
    data = cursor.fetchall()
    conn.close()
    return data

def delete_batch_expenses(expense_ids, current_email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in expense_ids)
    query = f"DELETE FROM expenses WHERE id IN ({placeholders}) AND student_email = ?"
    params = tuple(expense_ids) + (current_email,)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def create_student_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            student_email TEXT UNIQUE,
            password_hash TEXT  /* ✨ 新增密码栏位 */
        )
    """)
    conn.commit()
    conn.close()

def register_student(student_name, student_email, password_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (student_name, student_email, password_hash)
            VALUES (?, ?, ?)
        """, (student_name, student_email, password_hash))
        conn.commit()
    finally:
        conn.close()

def get_student_by_email(student_email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_email = ?", (student_email,))
    student = cursor.fetchone()
    conn.close()
    return student