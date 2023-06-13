from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
employee = Flask(__name__)
employee.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'

db = SQLAlchemy(employee)
migrate = Migrate(employee, db)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(100), nullable=False)

@employee.before_request
def create_tables():
    db.create_all()

@employee.route('/employee')
def employees():
    employees = Employee.query.all()
    return render_template('employee.html', employees=employees)

@employee.route('/create_employee', methods=['GET','POST'])
def create_employee():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        position = request.form['position']

        employee = Employee(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            position=position
        )

        db.session.add(employee)
        db.session.commit()

        return redirect(url_for('employees'))

    return render_template('create_employee.html')

@employee.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = Employee.query.get(employee_id)

    if request.method == "POST":
        employee.last_name = request.form['last_name']
        employee.first_name = request.form['first_name']
        employee.middle_name = request.form['middle_name']
        employee.position = request.form['position']

        db.session.commit()

        return redirect(url_for('employees'))

    return render_template('edit_employee.html', employee=employee)

@employee.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for('employees'))

if __name__ == '__main__':
    employee.run(port=5002)
