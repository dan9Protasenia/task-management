import unittest

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
        employee1 = Employee(last_name='Last 1', first_name='First 1', middle_name='Middle 1', position='Position 1')
        employee2 = Employee(last_name='Last 2', first_name='First 2', middle_name='Middle 2', position='Position 2')
        employee3 = Employee(last_name='Last 3', first_name='First 3', middle_name='Middle 3', position='Position 3')
        employee4 = Employee(last_name='Last 4', first_name='First 4', middle_name='Middle 4', position='Position 4')
        self.repository.create(employee1)
        self.repository.create(employee2)
        self.repository.create(employee3)
        self.repository.create(employee4)

        employees = get_all_employees()

        self.assertEqual(len(employees), 4)
        self.assertEqual(employees[0]['last_name'], 'Last 1')
        self.assertEqual(employees[0]['first_name'], 'First 1')
        self.assertEqual(employees[0]['middle_name'], 'Middle 1')
        self.assertEqual(employees[0]['position'], 'Position 1')
        self.assertEqual(employees[1]['last_name'], 'Last 2')
        self.assertEqual(employees[1]['first_name'], 'First 2')
        self.assertEqual(employees[1]['middle_name'], 'Middle 2')
        self.assertEqual(employees[1]['position'], 'Position 2')
        self.assertEqual(employees[2]['last_name'], 'Last 3')
        self.assertEqual(employees[2]['first_name'], 'First 3')
        self.assertEqual(employees[2]['middle_name'], 'Middle 3')
        self.assertEqual(employees[2]['position'], 'Position 3')
        self.assertEqual(employees[3]['last_name'], 'Last 4')
        self.assertEqual(employees[3]['first_name'], 'First 4')
        self.assertEqual(employees[3]['middle_name'], 'Middle 4')
        self.assertEqual(employees[3]['position'], 'Position 4')

    def test_create_employee(self):
        employee_data = {
            'last_name': 'Test Employee',
            'first_name': 'John',
            'middle_name': 'Doe',
            'position': 'Engineer'
        }

        create_employee(employee_data)

        employees = self.repository.get_all()

        self.assertIsNotNone(employees)
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].last_name, 'Test Employee')
        self.assertEqual(employees[0].first_name, 'John')
        self.assertEqual(employees[0].middle_name, 'Doe')
        self.assertEqual(employees[0].position, 'Engineer')

    def test_update_employee(self):
        employee = Employee(last_name='Last 1', first_name='First 1', middle_name='Middle 1', position='Position 1')
        self.repository.create(employee)

        data = {
            'last_name': 'Updated Last',
            'first_name': 'Updated First',
            'middle_name': 'Updated Middle',
            'position': 'Updated Position'
        }

        updated_employee = update_employee(employee.id, data)

        self.assertEqual(updated_employee.last_name, 'Updated Last')
        self.assertEqual(updated_employee.first_name, 'Updated First')
        self.assertEqual(updated_employee.middle_name, 'Updated Middle')
        self.assertEqual(updated_employee.position, 'Updated Position')

    def test_delete_employee(self):
        employee_data = {
            'last_name': 'Test Employee',
            'first_name': 'John',
            'middle_name': 'Doe',
            'position': 'Engineer'
        }
        employee = create_employee(employee_data)
        employee_id = employee.id

        result = delete_employee(employee_id)
        self.assertTrue(result)

        deleted_employee = self.repository.get_by_id(employee_id)
        self.assertIsNone(deleted_employee)


if __name__ == '__main__':
    unittest.main()
