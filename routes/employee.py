from flask import Blueprint, request, jsonify
from service.employee_repository import EmployeeRepository, Employee

employee = Blueprint('employee', __name__)
repository = EmployeeRepository()


@employee.route('/employee', methods=['GET'])
def employees():
    employees = repository.get_all()
    employee_list = []
    for employee in employees:
        employee_data = {
            'last_name': employee.last_name,
            'first_name': employee.first_name,
            'middle_name': employee.middle_name,
            'position': employee.position
        }
        employee_list.append(employee_data)

    return jsonify(employees=employee_list)


@employee.route('/create_employee', methods=['POST'])
def create_employee():
    data = request.get_json()
    last_name = data['last_name']
    first_name = data['first_name']
    middle_name = data['middle_name']
    position = data['position']

    employee = Employee(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        position=position
    )

    repository.create(employee)
    return jsonify(message='Employee created successfully')


@employee.route('/edit_employee/<int:employee_id>', methods=['PUT'])
def edit_employee(employee_id):
    employee = repository.get_by_id(employee_id)

    data = request.get_json()
    employee.last_name = data['last_name']
    employee.first_name = data['first_name']
    employee.middle_name = data['middle_name']
    employee.position = data['position']

    repository.update(employee)

    return jsonify(message='Employee update successfully')


@employee.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = repository.get_by_id(employee_id)
    repository.delete(employee)

    return jsonify(message='Project employee successfully')

