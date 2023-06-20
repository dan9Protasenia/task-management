import unittest
from datetime import date

from main import app, bd
from models.project_model import Project
from repository.project_repository import ProjectRepository
from service.project_service import get_all_projects, create_project, update_project, delete_project, project_to_dict, \
    repository


class ProjectServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()
        self.client = app.test_client()
        self.repository = ProjectRepository()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()

    def test_get_all_projects(self):
        project = Project(
            name='Test Project',
            short_name='TP',
            status='In Progress',
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 2, 1),
            actual_end_date=None,
            cost=1000.0,
            is_locked=False
        )
        bd.session.add(project)
        bd.session.commit()

        projects = get_all_projects()

        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['name'], 'Test Project')
        self.assertEqual(projects[0]['short_name'], 'TP')
        self.assertEqual(projects[0]['status'], 'In Progress')
        self.assertEqual(projects[0]['start_date'], '2023-01-01')
        self.assertEqual(projects[0]['planned_end_date'], '2023-02-01')
        self.assertIsNone(projects[0]['actual_end_date'])
        self.assertEqual(projects[0]['cost'], 1000.0)

    def test_create_project(self):
        data = {
            'name': 'New Project',
            'short_name': 'NP',
            'description': 'Test project',
            'planned_end_date': '2023-12-31',
            'cost': '2000.0',
            'status': 'In Progress'
        }

        project = create_project(data)

        self.assertIsNotNone(project.id)
        self.assertEqual(project.name, 'New Project')
        self.assertEqual(project.short_name, 'NP')
        self.assertEqual(project.description, 'Test project')
        self.assertEqual(project.planned_end_date, date(2023, 12, 31))
        self.assertIsNone(project.actual_end_date)
        self.assertEqual(project.cost, 2000.0)
        self.assertEqual(project.status, 'In Progress')

    def test_update_project(self):
        project = Project(
            name='Test Project',
            short_name='TP',
            status='In Progress',
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 2, 1),
            actual_end_date=None,
            cost=1000.0,
            is_locked=False
        )
        bd.session.add(project)
        bd.session.commit()

        data = {
            'name': 'Updated Project',
            'short_name': 'UP',
            'description': 'Updated test project',
            'planned_end_date': '2023-03-01',
            'cost': '1500.0',
            'status': 'Completed'
        }
        updated_project = update_project(project.id, data)

        self.assertEqual(updated_project.id, project.id)
        self.assertEqual(updated_project.name, 'Updated Project')
        self.assertEqual(updated_project.short_name, 'UP')
        self.assertEqual(updated_project.description, 'Updated test project')
        self.assertEqual(updated_project.planned_end_date, date(2023, 3, 1))
        self.assertIsNone(updated_project.actual_end_date)
        self.assertEqual(updated_project.cost, 1500.0)
        self.assertEqual(updated_project.status, 'Completed')

    def test_delete_project(self):
        project_data = {
            'name': 'Test Project',
            'short_name': 'TP',
            'description': 'Test project description',
            'start_date': date.today(),
            'planned_end_date': date.today().strftime('%Y-%m-%d'),
            'actual_end_date': None,
            'cost': 100.0,
            'status': 'In Progress'
        }
        project = create_project(project_data)
        project_id = project.id

        result = delete_project(project_id)
        self.assertTrue(result)

        deleted_project = repository.get_by_id(project_id)
        self.assertIsNone(deleted_project)

    def test_project_to_dict(self):
        project = Project(
            name='Test Project',
            short_name='TP',
            status='In Progress',
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 2, 1),
            actual_end_date=None,
            cost=1000.0,
            is_locked=False
        )

        project_dict = project_to_dict(project)

        self.assertEqual(project_dict['name'], 'Test Project')
        self.assertEqual(project_dict['short_name'], 'TP')
        self.assertEqual(project_dict['status'], 'In Progress')
        self.assertEqual(project_dict['start_date'], '2023-01-01')
        self.assertEqual(project_dict['planned_end_date'], '2023-02-01')
        self.assertIsNone(project_dict['actual_end_date'])
        self.assertEqual(project_dict['cost'], 1000.0)

if __name__ == '__main__':
    unittest.main()
