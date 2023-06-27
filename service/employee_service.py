from models.task_model import Task
from repository.employee_repository import EmployeeRepository, Employee

repository = EmployeeRepository()


def get_all_employees(search_query=None):
    employees = repository.get_all(search_query)
    employee_list = []
    for employee in employees:
        employee_data = {
            'last_name': employee.last_name,
            'first_name': employee.first_name,
            'middle_name': employee.middle_name,
            'position': employee.position,
            'id': employee.id
        }
        employee_list.append(employee_data)
    return employee_list


def create_employee(data):
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

    return employee


def update_employee(employee_id, data):
    employee = repository.get_by_id(employee_id)
    employee.last_name = data['last_name']
    employee.first_name = data['first_name']
    employee.middle_name = data['middle_name']
    employee.position = data['position']
    repository.update(employee)

    return employee


def delete_employee(employee_id):
    if is_employee_assigned_to_task(employee_id):
        return False, 'Cannot delete employee assigned to a task'

    employee = repository.get_by_id(employee_id)
    if employee:
        repository.delete(employee)
        return True, 'Employee deleted successfully'
    return False, 'Employee not found'


def is_employee_assigned_to_task(employee_id):
    task_count = Task.query.filter(Task.performers.any(id=employee_id)).count()
    return task_count > 0


def get_employees_by_position(position):
    employees = repository.get_all_by_position(position)
    employee_list = []
    for employee in employees:
        employee_data = {
            'last_name': employee.last_name,
            'first_name': employee.first_name,
            'middle_name': employee.middle_name,
            'position': employee.position,
            'id': employee.id
        }
        employee_list.append(employee_data)
    return employee_list
