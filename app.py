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

    # CHECK LOGIN
    if 'student_name' not in session:

        return redirect('/login')

    return render_template(
        'index.html',
        student_name=session['student_name']
    )


# =========================
# REGISTER PAGE
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        student_name = request.form.get(
            'student_name'
        )

        student_email = request.form.get(
            'student_email'
        )

        register_student(
            student_name,
            student_email
        )

        return redirect('/login')

    return render_template('register.html')


# =========================
# LOGIN PAGE
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        student_name = request.form.get(
            'student_name'
        )

        student_email = request.form.get(
            'student_email'
        )

        student = login_student(
            student_name,
            student_email
        )

        if student:

            session['student_name'] = student_name

            return redirect('/')

        else:

            return """
                <h1>Invalid Login</h1>

                <a href='/login'>
                    Try Again
                </a>
            """

    return render_template('login.html')


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():

    session.pop('student_name', None)

    return redirect('/login')


# =========================
# ADD EXPENSE PAGE
# =========================
@app.route('/add', methods=['GET', 'POST'])
def add_expense():

    # LOGIN REQUIRED
    if 'student_name' not in session:

        return redirect('/login')

    if request.method == 'POST':

        amount = request.form.get('amount')

        category = request.form.get('category')

        description = request.form.get('description')

        insert_expense(
            amount,
            category,
            description
        )

        return redirect(
            url_for('list_expenses')
        )

    return render_template('add.html')


# =========================
# VIEW EXPENSES
# =========================
@app.route('/list')
def list_expenses():

    # LOGIN REQUIRED
    if 'student_name' not in session:

        return redirect('/login')

    db_data = get_expenses()

    total_amount = 0

    formatted_expenses = []

    for row in db_data:

        total_amount += float(row[1])

        formatted_expenses.append([
            row[0],
            row[1],
            row[2],
            row[3]
        ])

    return render_template(
        'list.html',
        expenses=formatted_expenses,
        total=total_amount
    )


# =========================
# DELETE EXPENSE
# =========================
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):

    delete_expense(expense_id)

    return redirect(
        url_for('list_expenses')
    )


# =========================
# RUN FLASK
# =========================
if __name__ == '__main__':

    app.run(debug=True)


# =========================
# RUN CHART
# =========================

@app.route('/chart')
def chart():

    if 'student_name' not in session:
        return redirect('/login')

    expenses = get_expenses()

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