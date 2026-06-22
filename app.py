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

# ✨ UPDATE: 主页支持计算 Income，并动态调整余额！
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    current_name = session.get('student_name')
    import sqlite3

    if request.method == 'POST':
        new_budget = request.form.get('monthly_budget')
        if new_budget:
            conn = sqlite3.connect('expense.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET monthly_budget = ? WHERE student_email = ? OR student_name = ?", 
                           (float(new_budget), current_email, current_name))
            conn.commit()
            conn.close()
            flash(f"Success! Budget updated to RM {new_budget}", "success")
            return redirect('/')

    db_data = get_expenses(current_email)
    
    conn = sqlite3.connect('expense.db')
    cursor = conn.cursor()
    cursor.execute("SELECT monthly_budget FROM students WHERE student_email = ? OR student_name = ?", (current_email, current_name))
    budget_row = cursor.fetchone()
    conn.close()

    monthly_budget = float(budget_row[0]) if (budget_row and budget_row[0] is not None) else 500.0

    daily_total = 0
    monthly_total = 0
    monthly_income = 0  # ✨ 新增：本月总收入

    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")
    current_month_str = datetime.now().strftime("%Y-%m")

    for row in db_data:
        amt = float(row[1])
        date_str = row[5]
        trans_type = row[6] if len(row) > 6 else 'Expense' # ✨ 安全抓取类型

        if trans_type == 'Income':
            if date_str and date_str.startswith(current_month_str):
                monthly_income += amt
        else: # 默认是支出 Expense
            if date_str == today_str:
                daily_total += amt
            if date_str and date_str.startswith(current_month_str):
                monthly_total += amt

    # ✨ 核心算法升级：真实余额 = (初始预算 + 本月赚的钱) - 本月花的钱
    balance = (monthly_budget + monthly_income) - monthly_total
    abs_balance = abs(balance)
    
    budget_status = "normal"
    if balance < 0:
        budget_status = "danger"
    elif balance < ((monthly_budget + monthly_income) * 0.2):
        budget_status = "warning"

    return render_template('index.html', 
                           student_name=current_name,
                           daily_total=daily_total,
                           monthly_total=monthly_total,
                           monthly_income=monthly_income, # ✨ 传给前端
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
        trans_type = request.form.get('trans_type') # ✨ 获取是收入还是支出
        current_email = session.get('student_email')
        
        # 获取前端传来的日期，如果没有选，就用今天
        form_date = request.form.get('date')
        current_date = form_date if form_date else date.today().strftime("%Y-%m-%d")

        # 存入数据库
        insert_expense(amount, category, description, current_email, current_date, trans_type)
        flash(f"Successfully added {trans_type} of RM {amount}!", "success")
        return redirect(url_for('list_expenses'))

    return render_template('add.html')

from datetime import datetime 

@app.route('/list')
def list_expenses():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    db_data = get_expenses(current_email)
    
<<<<<<< HEAD
=======
    
>>>>>>> 2e75d307d0e1e618d462d511686dae2b013a2c7b
    total_amount = 0
    daily_total = 0
    monthly_total = 0
    formatted_expenses = []

<<<<<<< HEAD
    for row in db_data:
        amt = float(row[1])
        trans_type = row[6] if len(row) > 6 else 'Expense'
        
        # 只统计支出的总额用于显示
        if trans_type == 'Expense':
            total_amount += amt
            
        # 把类型 (trans_type) 加到列表的最后传给前端
        formatted_expenses.append([row[0], row[1], row[2], row[3], row[5], trans_type])
=======
    today_str = datetime.now().strftime("%Y-%m-%d")  # 比如 '2026-06-16'
    current_month_str = datetime.now().strftime("%Y-%m") # 比如 '2026-06'

    for row in db_data:
        amt = float(row[1])
        date_str = row[5] # 数据库里的 expense_date 是第 6 个栏位 (索引为 5)

        total_amount += amt
        
        # 判断是不是今天的消费
        if date_str == today_str:
            daily_total += amt
            
        # 判断是不是这个月的消费
        if date_str and date_str.startswith(current_month_str):
            monthly_total += amt

        # ✨ UPDATE: 把日期 (row[5]) 也加进列表里传给前端
        formatted_expenses.append([row[0], row[1], row[2], row[3], row[5]])

    return render_template('list.html', 
                           expenses=formatted_expenses, 
                           total=total_amount,
                           daily_total=daily_total,      # 传给前端
                           monthly_total=monthly_total)  # 传给前端
>>>>>>> 2e75d307d0e1e618d462d511686dae2b013a2c7b

    return render_template('list.html', 
                           expenses=formatted_expenses, 
                           total=total_amount)
    
# ✨ UPDATE: 新增数据可视化图表路由 (每日计算引擎)
@app.route('/chart')
def chart():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    db_data = get_expenses(current_email) # 拿数据库所有数据
    
    from datetime import datetime
    current_month_str = datetime.now().strftime("%Y-%m")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 准备空字典来做数据分类
    daily_expenses = {}
    category_expenses = {}
    monthly_total = 0
    daily_total = 0

    # 核心算法：循环每一笔账单，按天、按分类进行叠加
    for row in db_data:
        amt = float(row[1])
        category = row[2]
        date_str = row[5]
        trans_type = row[6] if len(row) > 6 else 'Expense'

        # 我们只把 "支出 (Expense)" 画进图表里，并且只看本月的数据
        if trans_type == 'Expense' and date_str and date_str.startswith(current_month_str):
            monthly_total += amt
            
            # 计算今天花了多少
            if date_str == today_str:
                daily_total += amt

            # 按照【日期】累加金额 (用于折线图和柱状图)
            if date_str in daily_expenses:
                daily_expenses[date_str] += amt
            else:
                daily_expenses[date_str] = amt
            
            # 按照【分类】累加金额 (用于饼图)
            if category in category_expenses:
                category_expenses[category] += amt
            else:
                category_expenses[category] = amt

    # 对日期进行排序 (确保图表从月初到月末按顺序走)
    sorted_dates = sorted(daily_expenses.keys())
    sorted_daily_amounts = [daily_expenses[d] for d in sorted_dates]

    categories = list(category_expenses.keys())
    category_amounts = list(category_expenses.values())

    # 把算好的数据传给前端的 chart.html
    return render_template('chart.html', 
                           dates=sorted_dates, 
                           daily_amounts=sorted_daily_amounts,
                           categories=categories,
                           category_amounts=category_amounts,
                           monthly_total=monthly_total,
                           daily_total=daily_total)


<<<<<<< HEAD
=======

>>>>>>> 2e75d307d0e1e618d462d511686dae2b013a2c7b
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