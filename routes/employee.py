from flask import Blueprint, request, jsonify, render_template

from service.employee_service import get_all_employees, create_employee, update_employee, delete_employee, \
    get_employees_by_position, get_employee

employee = Blueprint('employee', __name__)


@employee.route('/employees', methods=['GET'])
def get_employees():
    search_query = request.args.get('search_query')

    if search_query:
        employees = get_all_employees(search_query)
    else:
        employees = get_all_employees()

    if request.headers.get('Accept') == 'application/json':
        return jsonify(employees=employees)
    else:
        return render_template('employees.html', employees=employees)


@employee.route('/create_employee', methods=['POST', 'GET'])
def create_employee_route():
    if request.method == "POST":
        try:
            data = request.get_json()
            create_employee(data)
            return jsonify(message='Employee created successfully'), 201
        except Exception as e:
            return jsonify(message='Failed to create employee: ' + str(e)), 500
    else:
        return render_template('create_employee.html')

@employee.route('/edit_employee/<int:employee_id>', methods=['PUT', 'GET'])
def edit_employee_route(employee_id):
    if request.method == "PUT":
        data = request.get_json()
        update_employee(employee_id, data)
        return jsonify(message='Employee update successfully')
    else:
        employee_data = get_employee(employee_id)
        return render_template('edit_employee.html', employee=employee_data)


@employee.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    success, message = delete_employee(employee_id)
    if success:
        return jsonify(message=message)
    return jsonify(message=message), 400


@employee.route('/employees_by_position', methods=['GET'])
def get_employees_by_position_route():
    position = request.args.get('position')
    employees = get_employees_by_position(position)
    return jsonify(employees=employees)
