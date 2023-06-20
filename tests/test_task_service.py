import unittest
from datetime import date

from main import app, bd
from models.task_model import Task
from repository.task_repository import TaskRepository
from service.task_service import get_all_tasks, create_task, update_task, delete_task


class TaskServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()
        self.client = app.test_client()
        self.repository = TaskRepository()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()

    def test_get_all_tasks(self):
        task1 = Task(
            name='Task 1',
            priority='High',
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status='In Progress'
        )
        task2 = Task(
            name='Task 2',
            priority='Medium',
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status='In Progress'
        )
        task3 = Task(
            name='Task 3',
            priority='Low',
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status='In Progress'
        )
        self.repository.create(task1)
        self.repository.create(task2)
        self.repository.create(task3)

        tasks = get_all_tasks()

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]['name'], 'Task 1')
        self.assertEqual(tasks[0]['priority'], 'High')
        self.assertEqual(tasks[0]['start_date'], date.today().strftime('%Y-%m-%d'))
        self.assertEqual(tasks[0]['planned_end_date'], date.today().strftime('%Y-%m-%d'))
        self.assertIsNone(tasks[0]['actual_end_date'])
        self.assertEqual(tasks[0]['status'], 'In Progress')

    def test_create_task(self):
        data = {
            'name': 'New Task',
            'priority': 'High',
            'status': 'In Progress'
        }

        create_task(data)
        task = self.repository.get_all()[0]

        self.assertIsNotNone(task.id)
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.priority, 'High')
        self.assertEqual(task.start_date, date.today())
        self.assertEqual(task.planned_end_date, date.today())
        self.assertIsNone(task.actual_end_date)
        self.assertEqual(task.status, 'In Progress')

    def test_update_task(self):
        task = Task(
            name='Task 1',
            priority='High',
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status='In Progress'
        )
        self.repository.create(task)

        data = {
            'name': 'Updated Task',
            'priority': 'Medium',
            'status': 'Completed'
        }

        update_task(task.id, data)
        updated_task = self.repository.get_by_id(task.id)

        self.assertEqual(updated_task.name, 'Updated Task')
        self.assertEqual(updated_task.priority, 'Medium')
        self.assertEqual(updated_task.status, 'Completed')

    def test_delete_task(self):
        task_data = {
            'name': 'Test Task',
            'priority': 'High',
            'start_date': date.today(),
            'planned_end_date': date.today(),
            'actual_end_date': None,
            'status': 'In Progress'
        }
        task = Task(**task_data)
        self.repository.create(task)
        task_id = task.id

        delete_task(task_id)
        deleted_task = self.repository.get_by_id(task_id)

        self.assertIsNone(deleted_task)


if __name__ == '__main__':
    unittest.main()
