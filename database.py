import sqlite3

DB_NAME = "expense.db"

# ✨ UPDATE: 给数据库加上 type（收入/支出）属性，并加入防爆补丁
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
            expense_date TEXT,
            type TEXT DEFAULT 'Expense'  /* ✨ 新增：默认是支出 */
        )
    """)
    # 强行给旧表加上新栏位，旧账单自动变成 'Expense'，绝对不会报错！
    try:
        cursor.execute("ALTER TABLE expenses ADD COLUMN type TEXT DEFAULT 'Expense'")
    except:
        pass
    conn.commit()
    conn.close()

# ✨ UPDATE: 插入数据时，接收 trans_type (Income 还是 Expense)
def insert_expense(amount, category, description, student_email, expense_date, trans_type='Expense'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, description, student_email, expense_date, type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (amount, category, description, student_email, expense_date, trans_type))
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

# ✨ UPDATE: 这里是带有 monthly_budget 的新图纸！
def create_student_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            student_email TEXT UNIQUE,
            password_hash TEXT,
            monthly_budget REAL DEFAULT 500.0
        )
    """)
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN monthly_budget REAL DEFAULT 500.0")
    except:
        pass
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

# ✨ UPDATE: 更新预算的新功能
def update_student_budget(student_email, new_budget):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET monthly_budget = ? WHERE student_email = ?", (new_budget, student_email))
    conn.commit()
    conn.close()