from flask import Blueprint, request, jsonify
from service.employee_service import get_all_employees, create_employee, update_employee, delete_employee, get_employees_by_position
from service.job_service import get_employees_by_job
employee = Blueprint('employee', __name__)


@employee.route('/employees', methods=['GET'])
def get_employees():
    search_query = request.args.get('search_query')

    if search_query:
        employees = get_all_employees(search_query)
    else:
        employees = get_all_employees()

    return jsonify(employees=employees)


@employee.route('/create_employee', methods=['POST'])
def create_employee_route():
    data = request.get_json()
    employee = create_employee(data)
    if employee:
        employee_data = {
            'last_name': employee.last_name,
            'first_name': employee.first_name,
            'middle_name': employee.middle_name,
            'position': employee.position,
            'id': employee.id
        }
        return jsonify(message='Employee created successfully'), 201
    return jsonify(message='Failed to create employee'), 400



@employee.route('/edit_employee/<int:employee_id>', methods=['PUT'])
def edit_employee_route(employee_id):
    data = request.get_json()
    employee = update_employee(employee_id, data)
    if employee:
        return jsonify(message='Employee updated successfully', employee=employee)
    return jsonify(message='Employee not found'), 404


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

@employee.route('/employees_by_job/<int:job_id>', methods=['GET'])
def get_employees_by_job_route(job_id):
    print(f"Fetching employees for job ID: {job_id}")
    employees = get_employees_by_job(job_id)
    print(f"Found employees: {employees}")
    return jsonify(employees=employees)