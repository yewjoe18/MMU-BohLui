from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

mock_database = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        
        mock_database.append([amount, category, description])
        
        return redirect(url_for('list_expenses'))
    
    return render_template('add.html')

@app.route('/list')
def list_expenses():
    total_amount = 0
    for expense in mock_database:
        total_amount += float(expense[0])
        
    return render_template('list.html', expenses=mock_database, total=total_amount)

if __name__ == '__main__':
    app.run(debug=True)