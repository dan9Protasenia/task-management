from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from service.employee_service import get_all_employees, create_employee, update_employee, delete_employee

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
    create_employee(data)
    return jsonify(message='Employee created successfully')


@employee.route('/edit_employee/<int:employee_id>', methods=['PUT'])
def edit_employee_route(employee_id):
    data = request.get_json()
    update_employee(employee_id, data)
    return jsonify(message='Employee updated successfully')


@employee.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    delete_employee(employee_id)
    return jsonify(message='Employee deleted successfully')
