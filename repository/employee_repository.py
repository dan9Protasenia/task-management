from models.employee_model import Employee
from models.employee_model import bd
from . import AbstractRepository


class EmployeeRepository(AbstractRepository):
    def get_all(self):
        return Employee.query.filter_by(is_locked=False).all()

    def get_by_id(self, project_id):
        return Employee.query.filter_by(id=project_id, is_locked=False).first()

    def create(self, project):
        bd.session.add(project)
        bd.session.commit()

    def update(self, project):
        bd.session.commit()

    def delete(self, project):
        bd.session.delete(project)
        bd.session.commit()
