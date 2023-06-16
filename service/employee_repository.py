from models.employee_model import bd
from models.employee_model import Employee
from . import AbstractRepository

class EmployeeRepository(AbstractRepository):
    def get_all(self):
        return Employee.query.all()

    def get_by_id(self, task_id):
        return Employee.query.get(task_id)

    def create(self, employee):
        bd.session.add(employee)
        bd.session.commit()

    def update(self, employee):
        bd.session.commit()

    def delete(self, employee):
        bd.session.delete(employee)
        bd.session.commit()
