import sqlite3

# Connect to SQLite database (creates company.db if it does not exist)
connection = sqlite3.connect('company.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create tables if they do not already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS department (
    id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY,
    name TEXT,
    deptid INTEGER
)
''')

# Clear old data so each run has exactly 5 records in each table
cursor.execute('DELETE FROM employee')
cursor.execute('DELETE FROM department')

# Insert department records
# This helps later with INNER JOIN, LEFT JOIN, and RIGHT JOIN examples.
departments = [
    (1, 'HR', 'Bangalore'),
    (2, 'IT', 'Pune'),
    (3, 'Finance', 'Mumbai'),
    (4, 'Sales', 'Delhi'),
    (5, 'Operations', 'Chennai')
]

for dept in departments:
    cursor.execute(
        'INSERT INTO department (id, name, location) VALUES (?, ?, ?)',
        dept
    )

# Insert employee records
# One employee has a department that does not exist (deptid 99)
# One department (Sales) has no employees assigned to it
employees = [
    (1, 'Alice', 1),
    (2, 'Bob', 2),
    (3, 'Charlie', 99),
    (4, 'Diana', 3),
    (5, 'Eve', 5)
]

for emp in employees:
    cursor.execute(
        'INSERT INTO employee (id, name, deptid) VALUES (?, ?, ?)',
        emp
    )

# Save the changes to the database
connection.commit()

# Execute SQL to fetch all employee records
cursor.execute('SELECT id, name, deptid FROM employee ORDER BY id')
employee_rows = cursor.fetchall()

# Execute SQL to fetch all department records
cursor.execute('SELECT id, name, location FROM department ORDER BY id')
department_rows = cursor.fetchall()

# Print employee records in a student-friendly format
print('Employees:')
print('ID | Name    | DeptID')
print('---+---------+-------')
for emp_id, name, deptid in employee_rows:
    print(f'{emp_id}  | {name:<7} | {deptid}')

print('\nDepartments:')
print('ID | Name       | Location')
print('---+------------+-----------')
for dept_id, name, location in department_rows:
    print(f'{dept_id}  | {name:<10} | {location}')

# Query to show the names of employees who work in the HR department
cursor.execute('''
SELECT e.name
FROM employee e
JOIN department d ON e.deptid = d.id
WHERE d.name = 'HR'
ORDER BY e.id
''')
hr_employees = cursor.fetchall()

print('\nEmployees in HR Department:')
if hr_employees:
    print('Name')
    for (name,) in hr_employees:
        print(name)
else:
    print('No employees found in HR department.')

# Close the cursor and database connection
cursor.close()
connection.close()