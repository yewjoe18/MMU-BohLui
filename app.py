from flask import Flask, render_template, request, redirect, url_for
from database import create_table, insert_expense, get_expenses

app = Flask(__name__)
create_table()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        
        insert_expense(amount, category, description)
        
        return redirect(url_for('list_expenses'))
    
    return render_template('add.html')

@app.route('/list')
def list_expenses():
    db_data =get_expenses()
    total_amount = 0
    formatted_expenses=[]
    for row in db_data:
        total_amount += float(row[1])
        formatted_expenses.append([row[1],row[2],row[3]])
        
    return render_template('list.html', expenses=formatted_expenses, total=total_amount)

if __name__ == '__main__':
    app.run(debug=True)