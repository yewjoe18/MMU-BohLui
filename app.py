from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import *

app = Flask(__name__)
app.secret_key = "bohlui_secret_key"

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30) 

create_table()
create_student_table()

@app.route('/')
def home():
    if 'student_name' not in session:
        return redirect('/login')
    return render_template('index.html', student_name=session['student_name'])

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
<<<<<<< HEAD
            # register successful
            flash("Account created successfully! Please login.", "success")
            return redirect('/login')
        except:
            # register unsuccessful
=======
            # 注册成功，发送成功消息
            flash("Account created successfully! Please login.", "success")
            return redirect('/login')
        except:
            # 注册失败（邮箱重复），发送错误消息，留在本页
>>>>>>> 956bb04f2a114a18e4712e70b44b95f999b758dc
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
<<<<<<< HEAD
            # login fail
=======
            # 登录失败，发送错误消息，留在本页
>>>>>>> 956bb04f2a114a18e4712e70b44b95f999b758dc
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

<<<<<<< HEAD
from datetime import datetime 

=======
>>>>>>> 956bb04f2a114a18e4712e70b44b95f999b758dc
@app.route('/list')
def list_expenses():
    if 'student_name' not in session:
        return redirect('/login')

    current_email = session.get('student_email')
    db_data = get_expenses(current_email)
<<<<<<< HEAD
    
    
    total_amount = 0
    daily_total = 0
    monthly_total = 0
    formatted_expenses = []

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
=======
    total_amount = 0
    formatted_expenses = []

    for row in db_data:
        total_amount += float(row[1])
        formatted_expenses.append([row[0], row[1], row[2], row[3]])

    return render_template('list.html', expenses=formatted_expenses, total=total_amount)
>>>>>>> 956bb04f2a114a18e4712e70b44b95f999b758dc

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