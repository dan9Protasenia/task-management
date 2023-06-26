from models.employee_model import Employee
from models.employee_model import bd
from . import AbstractRepository
from sqlalchemy import or_

class EmployeeRepository(AbstractRepository):
    def get_all(self, search_query=None):
        if search_query:
            return Employee.query.filter(
                or_(
                    Employee.last_name.ilike(f'%{search_query}%'),
                    Employee.first_name.ilike(f'%{search_query}%'),
                    Employee.middle_name.ilike(f'%{search_query}%')
                ),
                Employee.is_locked == False
            ).all()
        else:
            return Employee.query.filter_by(is_locked=False).all()

    def get_by_id(self, employee_id):
        return Employee.query.filter_by(id=employee_id, is_locked=False).first()

    def create(self, employee):
        bd.session.add(employee)
        bd.session.commit()

    def update(self, employee):
        bd.session.commit()

    def delete(self, employee):
        if employee:
            bd.session.delete(employee)
            bd.session.commit()
            return True
        return False
