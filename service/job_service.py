from models.employee_model import Employee
from repository.job_repository import JobRepository, Job

repository = JobRepository()


def get_all_jobs():
    jobs = repository.get_all()
    job_list = []
    for job in jobs:
        job_data = {
            'name_position': job.name_position,
            'tariff_rate': job.tariff_rate,
            'assigned_employees': get_assigned_employees(job.id),
            'id':job.id
        }
        job_list.append(job_data)
    return job_list


def create_job(data):
    name_position = data['name_position']
    tariff_rate = data['tariff_rate']

    job = Job(
        name_position=name_position,
        tariff_rate=tariff_rate
    )

    repository.create(job)
    return job


def update_job(job_id, data):
    job = repository.get_by_id(job_id)
    job.name_position = data['name_position']
    job.tariff_rate = data['tariff_rate']
    repository.update(job)

    return job


def delete_job(job_id):
    job = repository.get_by_id(job_id)
    if job:
        repository.delete(job)
        return True
    return False


def get_assigned_employees(job_id):
    employees = Employee.query.filter(Employee.position == job_id).all()
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


def get_employees_by_job(job_id):
    employees = repository.get_employees(job_id)
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
