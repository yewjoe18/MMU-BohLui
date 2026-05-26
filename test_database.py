from database import *

# create table
create_table()

# insert sample data
insert_expense(12.5, "Food", "Lunch")
insert_expense(5.0, "Transport", "Bus fare")

# retrieve data
expenses = get_expenses()

print(expenses)