import unittest
from datetime import date, datetime

from constants import (
    STATUS_IN_PROGRESS,
    STATUS_COMPLETED,
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

        tasks_project1 = get_all_tasks(task1.project_id)
        tasks_project2 = get_all_tasks(task2.project_id)
        tasks_project3 = get_all_tasks(task3.project_id)

        self.assertEqual(len(tasks_project1), 1)
        self.assertEqual(tasks_project1[0]['name'], TASK1)
        self.assertEqual(tasks_project1[0]['priority'], PRIORITY_HIGH)
        self.assertEqual(tasks_project1[0]['start_date'], date.today().strftime('%Y-%m-%d'))
        self.assertEqual(tasks_project1[0]['planned_end_date'], date.today().strftime('%Y-%m-%d'))
        self.assertIsNone(tasks_project1[0]['actual_end_date'])
        self.assertEqual(tasks_project1[0]['status'], STATUS_IN_PROGRESS)

        self.assertEqual(len(tasks_project2), 1)
        self.assertEqual(tasks_project2[0]['name'], TASK2)
        self.assertEqual(tasks_project2[0]['priority'], PRIORITY_MEDIUM)
        self.assertEqual(tasks_project2[0]['start_date'], date.today().strftime('%Y-%m-%d'))
        self.assertEqual(tasks_project2[0]['planned_end_date'], date.today().strftime('%Y-%m-%d'))
        self.assertIsNone(tasks_project2[0]['actual_end_date'])
        self.assertEqual(tasks_project2[0]['status'], STATUS_IN_PROGRESS)

        self.assertEqual(len(tasks_project3), 1)
        self.assertEqual(tasks_project3[0]['name'], TASK3)
        self.assertEqual(tasks_project3[0]['priority'], PRIORITY_LOW)
        self.assertEqual(tasks_project3[0]['start_date'], date.today().strftime('%Y-%m-%d'))
        self.assertEqual(tasks_project3[0]['planned_end_date'], date.today().strftime('%Y-%m-%d'))
        self.assertIsNone(tasks_project3[0]['actual_end_date'])
        self.assertEqual(tasks_project3[0]['status'], STATUS_IN_PROGRESS)

    def test_create_task(self):
        project_id = 1
        data = {
            'name': 'New Task',
            'priority': 'High',
            'status': 'In Progress',
            'planned_end_date': '2023-07-20'
        }

        create_task(project_id, data)
        task = self.repository.get_all()[0]

        self.assertIsNotNone(task.id)
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.priority, 'High')
        self.assertEqual(task.start_date, date.today())
        self.assertEqual(task.planned_end_date, datetime.strptime(data['planned_end_date'], '%Y-%m-%d').date())
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


# def setUp(self):
#     app.testing = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#     self.app_context = app.app_context()
#     self.app_context.push()
#     bd.create_all()
#     self.client = app.test_client()
#     self.repository = TaskRepository()

#
# def tearDown(self):
#     bd.session.remove()
#     bd.drop_all()


if __name__ == '__main__':
    unittest.main()
