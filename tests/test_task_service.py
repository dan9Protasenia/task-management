import unittest
from datetime import date

from constants import (
    STATUS_IN_PROGRESS,
    STATUS_COMPLETED,
    TASK_NEW,
    TASK_UPDATED,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
    TASK1,
    TASK2,
    TASK3
)
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
            name=TASK1,
            priority=PRIORITY_HIGH,
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS,
            project_id='1'
        )
        task2 = Task(
            name=TASK2,
            priority=PRIORITY_MEDIUM,
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS,
            project_id='2'
        )
        task3 = Task(
            name=TASK3,
            priority=PRIORITY_LOW,
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS,
            project_id='3'
        )
        self.repository.create(task1)
        self.repository.create(task2)
        self.repository.create(task3)

        tasks = get_all_tasks()

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]['name'], TASK1)
        self.assertEqual(tasks[0]['priority'], PRIORITY_HIGH)
        self.assertEqual(tasks[0]['start_date'], date.today().strftime('%Y-%m-%d'))
        self.assertEqual(tasks[0]['planned_end_date'], date.today().strftime('%Y-%m-%d'))
        self.assertIsNone(tasks[0]['actual_end_date'])
        self.assertEqual(tasks[0]['status'], STATUS_IN_PROGRESS)


    def test_create_task(self):
        project_id = 1
        data = {
            'name': 'New Task',
            'priority': 'High',
            'status': 'In Progress'

        }



        create_task(project_id, data)
        task = self.repository.get_all()[0]

        self.assertIsNotNone(task.id)
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.priority, 'High')
        self.assertEqual(task.start_date, date.today())
        self.assertEqual(task.planned_end_date, date.today())
        self.assertIsNone(task.actual_end_date)
        self.assertEqual(task.status, 'In Progress')
        self.assertEqual(task.project_id, 1)


    def test_update_task(self):
        task = Task(
            name=TASK1,
            priority=PRIORITY_HIGH,
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS
        )
        self.repository.create(task)

        data = {
            'name': TASK_UPDATED,
            'priority': PRIORITY_MEDIUM,
            'status': STATUS_COMPLETED
        }

        update_task(task.id, data)
        updated_task = self.repository.get_by_id(task.id)

        self.assertEqual(updated_task.name, TASK_UPDATED)
        self.assertEqual(updated_task.priority, PRIORITY_MEDIUM)
        self.assertEqual(updated_task.status, STATUS_COMPLETED)

    def test_delete_task(self):
        task_data = {
            'name': TASK1,
            'priority': PRIORITY_HIGH,
            'start_date': date.today(),
            'planned_end_date': date.today(),
            'actual_end_date': None,
            'status': STATUS_IN_PROGRESS
        }
        task = Task(**task_data)
        self.repository.create(task)
        task_id = task.id

        delete_task(task_id)
        deleted_task = self.repository.get_by_id(task_id)

        self.assertIsNone(deleted_task)

    def test_get_all_tasks_with_filters(self):
        task1 = Task(
            name=TASK1,
            priority=PRIORITY_HIGH,
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 1, 5),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS,
            project_id='1'
        )
        task2 = Task(
            name=TASK2,
            priority=PRIORITY_MEDIUM,
            start_date=date(2023, 1, 2),
            planned_end_date=date(2023, 1, 7),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS,
            project_id='1'
        )
        task3 = Task(
            name=TASK3,
            priority=PRIORITY_LOW,
            start_date=date(2023, 1, 3),
            planned_end_date=date(2023, 1, 9),
            actual_end_date=None,
            status=STATUS_COMPLETED,
            project_id='1'
        )
        self.repository.create(task1)
        self.repository.create(task2)
        self.repository.create(task3)

        # Test filtering by name
        response = self.client.get('/tasks/1?name=Task 1')
        data = response.get_json()
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['name'], TASK1)

        # Test filtering by start date
        response = self.client.get('/tasks/1?start_date_from=2023-01-02&start_date_to=2023-01-04')
        data = response.get_json()
        self.assertEqual(len(data['tasks']), 2)
        self.assertEqual(data['tasks'][0]['name'], TASK1)
        self.assertEqual(data['tasks'][1]['name'], TASK2)

        response = self.client.get('/tasks/1?end_date_from=2023-01-06&end_date_to=2023-01-08')
        data = response.get_json()
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['name'], TASK2)

        response = self.client.get('/tasks/1?status=Completed')
        data = response.get_json()
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['name'], TASK3)


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



if __name__ == '__main__':
    unittest.main()
