from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import *

app = Flask(__name__)
app.secret_key = "bohlui_secret_key"

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30) 

create_table()
create_student_table()

from datetime import datetime # 确保最上面有这行

# ✨ UPDATE: 把主页路由升级，支持接收预算修改，并计算所有看板数据
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')

    # 处理用户在主页修改预算的请求
    if request.method == 'POST':
        new_budget = request.form.get('monthly_budget')
        if new_budget:
            update_student_budget(current_email, float(new_budget))
            flash("Budget updated successfully!", "success")
            return redirect(url_for('home'))

    # 获取数据库数据
    db_data = get_expenses(current_email)
    student_data = get_student_by_email(current_email)
    monthly_budget = student_data[4] if student_data and len(student_data) > 4 else 500.0

    daily_total = 0
    monthly_total = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    current_month_str = datetime.now().strftime("%Y-%m")

    for row in db_data:
        amt = float(row[1])
        date_str = row[5]
        if date_str == today_str:
            daily_total += amt
        if date_str and date_str.startswith(current_month_str):
            monthly_total += amt

    # 计算余额与预警状态
    balance = monthly_budget - monthly_total
    abs_balance = abs(balance)
    
    budget_status = "normal"
    if balance < 0:
        budget_status = "danger"
    elif balance < (monthly_budget * 0.2):
        budget_status = "warning"

    # 把所有数据传给 index.html
    return render_template('index.html', 
                           student_name=session['student_name'],
                           daily_total=daily_total,
                           monthly_total=monthly_total,
                           monthly_budget=monthly_budget,
                           balance=balance,
                           abs_balance=abs_balance,
                           budget_status=budget_status)
# =========================
# REGISTER PAGE
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('student_name')
        email = request.form.get('student_email')
        password = request.form.get('password')
        
        hashed_pwd = generate_password_hash(password)
        
        try:
            register_student(name, email, hashed_pwd)
            # register successful
            flash("Account created successfully! Please login.", "success")
            return redirect('/login')
        except:
            # register unsuccessful
            flash("Email Already Registered! Please try a different one.", "error")
            return redirect('/register')
            
    return render_template('register.html')

# =========================
# LOGIN PAGE
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('student_email')
        password = request.form.get('password')

        student = get_student_by_email(email)
        
        if student and check_password_hash(student[3], password):
            session.permanent = True
            session['student_name'] = student[1]
            session['student_email'] = student[2]
            return redirect('/')
        else:
            # login fail
            flash("Invalid Email or Password. Please try again.", "error")
            return redirect('/login')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('student_name', None)
    session.pop('student_email', None)
    return redirect('/login')

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

from datetime import datetime 

# ✨ UPDATE: 极简版的 list 路由，去掉了所有不需要的预算计算逻辑
@app.route('/list')
def list_expenses():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    
    # 1. 拿数据库里的所有账单
    db_data = get_expenses(current_email)
    
    total_amount = 0
    formatted_expenses = []

    # 2. 算总额，并整理表格数据
    for row in db_data:
        total_amount += float(row[1])
        # 注意：这里依然要把 row[5] (日期) 放进去，保证你的 Expense Records 表格能显示日期！
        formatted_expenses.append([row[0], row[1], row[2], row[3], row[5]])

    # 3. 只传表格数据和总金额给 list.html
    return render_template('list.html', 
                           expenses=formatted_expenses, 
                           total=total_amount)
    
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

    return render_template('chart.html', categories=categories, amounts=amounts)


@app.route('/delete_batch', methods=['POST'])
def delete_batch():
    if 'student_name' not in session:
        return redirect('/login')
        
    selected_ids = request.form.getlist('expense_ids')
    if selected_ids:
        current_email = session.get('student_email')
        delete_batch_expenses(selected_ids, current_email)
        
    return redirect(url_for('list_expenses'))

if __name__ == '__main__':
    app.run(debug=True)