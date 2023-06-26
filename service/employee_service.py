from repository.employee_repository import EmployeeRepository, Employee

repository = EmployeeRepository()


def get_all_employees(search_query=None):
    employees = repository.get_all()

    if search_query:
        filtered_employees = []
        for employee in employees:
            if search_query.lower() in employee.last_name.lower() or \
                    search_query.lower() in employee.first_name.lower() or \
                    search_query.lower() in employee.middle_name.lower():
                employee_data = {
                    'last_name': employee.last_name,
                    'first_name': employee.first_name,
                    'middle_name': employee.middle_name,
                    'position': employee.position
                }
                filtered_employees.append(employee_data)
        return filtered_employees
    else:
        employee_list = []
        for employee in employees:
            employee_data = {
                'last_name': employee.last_name,
                'first_name': employee.first_name,
                'middle_name': employee.middle_name,
                'position': employee.position
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
    employee = repository.get_by_id(employee_id)
    repository.delete(employee)
    return employee
