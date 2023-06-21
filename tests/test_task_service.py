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
            status=STATUS_IN_PROGRESS
        )
        task2 = Task(
            name=TASK2,
            priority=PRIORITY_MEDIUM,
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS
        )
        task3 = Task(
            name=TASK3,
            priority=PRIORITY_LOW,
            start_date=date.today(),
            planned_end_date=date.today(),
            actual_end_date=None,
            status=STATUS_IN_PROGRESS
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
        data = {
            'name': TASK_NEW,
            'priority': PRIORITY_HIGH,
            'status': STATUS_IN_PROGRESS
        }

        create_task(data)
        task = self.repository.get_all()[0]

        self.assertIsNotNone(task.id)
        self.assertEqual(task.name, TASK_NEW)
        self.assertEqual(task.priority, PRIORITY_HIGH)
        self.assertEqual(task.start_date, date.today())
        self.assertEqual(task.planned_end_date, date.today())
        self.assertIsNone(task.actual_end_date)
        self.assertEqual(task.status, STATUS_IN_PROGRESS
                         )

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


if __name__ == '__main__':
    unittest.main()
