from datetime import date
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from database import *

app = Flask(__name__)

# =========================
# SECRET KEY
# =========================
app.secret_key = "bohlui_secret_key"

# =========================
# CREATE DATABASE TABLES
# =========================
create_table()
create_student_table()

# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    if 'student_name' not in session:
        return redirect('/login')
    return render_template(
        'index.html',
        student_name=session['student_name']
    )

# =========================
# REGISTER PAGE (修复了重复注册闪退)
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_email = request.form.get('student_email')
        
        try:
            register_student(student_name, student_email)
            return redirect('/login')
        except:
            # 如果数据库报错（比如邮箱重复），就会跳到这里
            return """
                <h1>Email Already Registered!</h1>
                <a href='/register'>Try a different email</a>
            """
    return render_template('register.html')

# =========================
# LOGIN PAGE
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_email = request.form.get('student_email')

        student = login_student(student_name, student_email)

        if student:
            session['student_name'] = student_name
            session['student_email'] = student_email
            return redirect('/')
        else:
            return """
                <h1>Invalid Login</h1>
                <a href='/login'>Try Again</a>
            """
    return render_template('login.html')

# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.pop('student_name', None)
    session.pop('student_email', None)
    return redirect('/login')

# =========================
# ADD EXPENSE PAGE
# =========================
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if 'student_name' not in session:
        return redirect('/login')

    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        
        current_email = session.get('student_email')
        current_date = date.today().strftime("%Y-%m-%d")

        insert_expense(amount, category, description, current_email, current_date)
        return redirect(url_for('list_expenses'))

    return render_template('add.html')

# =========================
# VIEW EXPENSES
# =========================
# =========================
# VIEW EXPENSES
# =========================
@app.route('/list')
def list_expenses():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    db_data = get_expenses(current_email) 
    total_amount = 0
    formatted_expenses = []

    for row in db_data:
        total_amount += float(row[1])
        formatted_expenses.append([row[0], row[1], row[2], row[3]])

    return render_template(
        'list.html',
        expenses=formatted_expenses,
        total=total_amount
    )

# =========================
# CHART PAGE (提上来了！)
# =========================
# =========================
# CHART PAGE
# =========================
@app.route('/chart')
def chart():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    expenses = get_expenses(current_email)

    categories = []
    amounts = []

    for expense in expenses:
        categories.append(expense[2])
        amounts.append(expense[1])

    return render_template(
        'chart.html',
        categories=categories,
        amounts=amounts
    )

# =========================
# DELETE EXPENSE
# =========================
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    if 'student_name' not in session:
        return redirect('/login')
        
    delete_expense(expense_id)
    return redirect(url_for('list_expenses'))

# =========================
# RUN FLASK (必须在最底端！)
# =========================
if __name__ == '__main__':
    app.run(debug=True)