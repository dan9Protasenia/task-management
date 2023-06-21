import unittest

from constants import (
    LAST_NAME_1,
    LAST_NAME_2,
    LAST_NAME_3,
    LAST_NAME_4,
    LAST_NAME_UPDATED,
    LAST_NAME_TEST,
    FIRST_NAME_1,
    FIRST_NAME_2,
    FIRST_NAME_3,
    FIRST_NAME_4,
    FIRST_NAME_JOHN,
    FIRST_NAME_UPDATED,
    MIDDLE_NAME_1,
    MIDDLE_NAME_2,
    MIDDLE_NAME_3,
    MIDDLE_NAME_4,
    MIDDLE_NAME_DOE,
    MIDDLE_NAME_UPDATED,
    POSITION_1,
    POSITION_2,
    POSITION_3,
    POSITION_4,
    POSITION_ENGINEER,
    POSITION_UPDATED
)
from main import app, bd
from models.employee_model import Employee
from repository.employee_repository import EmployeeRepository
from service.employee_service import get_all_employees, create_employee, update_employee, delete_employee


class EmployeeServiceTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()
        self.client = app.test_client()
        self.repository = EmployeeRepository()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()

    def test_get_all_employees(self):
        employee1 = Employee(last_name=LAST_NAME_1, first_name=FIRST_NAME_1, middle_name=MIDDLE_NAME_1,
                             position=POSITION_1)
        employee2 = Employee(last_name=LAST_NAME_2, first_name=FIRST_NAME_2, middle_name=MIDDLE_NAME_2,
                             position=POSITION_2)
        employee3 = Employee(last_name=LAST_NAME_3, first_name=FIRST_NAME_3, middle_name=MIDDLE_NAME_3,
                             position=POSITION_3)
        employee4 = Employee(last_name=LAST_NAME_4, first_name=FIRST_NAME_4, middle_name=MIDDLE_NAME_4,
                             position=POSITION_4)
        self.repository.create(employee1)
        self.repository.create(employee2)
        self.repository.create(employee3)
        self.repository.create(employee4)

        employees = get_all_employees()

        self.assertEqual(len(employees), 4)
        self.assertEqual(employees[0]['last_name'], LAST_NAME_1)
        self.assertEqual(employees[0]['first_name'], FIRST_NAME_1)
        self.assertEqual(employees[0]['middle_name'], MIDDLE_NAME_1)
        self.assertEqual(employees[0]['position'], POSITION_1)
        self.assertEqual(employees[1]['last_name'], LAST_NAME_2)
        self.assertEqual(employees[1]['first_name'], FIRST_NAME_2)
        self.assertEqual(employees[1]['middle_name'], MIDDLE_NAME_2)
        self.assertEqual(employees[1]['position'], POSITION_2)
        self.assertEqual(employees[2]['last_name'], LAST_NAME_3)
        self.assertEqual(employees[2]['first_name'], FIRST_NAME_3)
        self.assertEqual(employees[2]['middle_name'], MIDDLE_NAME_3)
        self.assertEqual(employees[2]['position'], POSITION_3)
        self.assertEqual(employees[3]['last_name'], LAST_NAME_4)
        self.assertEqual(employees[3]['first_name'], FIRST_NAME_4)
        self.assertEqual(employees[3]['middle_name'], MIDDLE_NAME_4)
        self.assertEqual(employees[3]['position'], POSITION_4)

    def test_create_employee(self):
        employee_data = {
            'last_name': LAST_NAME_TEST,
            'first_name': FIRST_NAME_JOHN,
            'middle_name': MIDDLE_NAME_DOE,
            'position': POSITION_ENGINEER
        }

        create_employee(employee_data)

        employees = self.repository.get_all()

        self.assertIsNotNone(employees)
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].last_name, LAST_NAME_TEST)
        self.assertEqual(employees[0].first_name, FIRST_NAME_JOHN)
        self.assertEqual(employees[0].middle_name, MIDDLE_NAME_DOE)
        self.assertEqual(employees[0].position, POSITION_ENGINEER)

    def test_update_employee(self):
        employee = Employee(last_name=LAST_NAME_1, first_name=FIRST_NAME_1, middle_name=MIDDLE_NAME_1,
                            position=POSITION_1)
        self.repository.create(employee)

        data = {
            'last_name': LAST_NAME_UPDATED,
            'first_name': FIRST_NAME_UPDATED,
            'middle_name': MIDDLE_NAME_UPDATED,
            'position': POSITION_UPDATED
        }

        updated_employee = update_employee(employee.id, data)

        self.assertEqual(updated_employee.last_name, LAST_NAME_UPDATED)
        self.assertEqual(updated_employee.first_name, FIRST_NAME_UPDATED)
        self.assertEqual(updated_employee.middle_name, MIDDLE_NAME_UPDATED)
        self.assertEqual(updated_employee.position, POSITION_UPDATED)

    def test_delete_employee(self):
        employee_data = {
            'last_name': LAST_NAME_TEST,
            'first_name': FIRST_NAME_JOHN,
            'middle_name': MIDDLE_NAME_DOE,
            'position': POSITION_ENGINEER
        }
        employee = create_employee(employee_data)
        employee_id = employee.id

        result = delete_employee(employee_id)
        self.assertTrue(result)

        deleted_employee = self.repository.get_by_id(employee_id)
        self.assertIsNone(deleted_employee)


if __name__ == '__main__':
    unittest.main()
