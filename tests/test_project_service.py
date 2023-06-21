import unittest
from datetime import date

from constants import (
    STATUS_IN_PROGRESS,
    STATUS_COMPLETED,
    PROJECT_NEW,
    PROJECT_TEST,
    PROJECT_UPDATED,
    SHORT_NAME_NEW,
    SHORT_NAME_TEST,
    SHORT_NAME_UPDATED,
    DESCRIPTION_TEST,
    DESCRIPTION_UPDATED,
    DESCRIPTION_TEST_PROJECT,
    START_DATE_TEST,
    PLANNED_END_DATE,
    COST_1000,
    COST_1500,
    COST_2000,
    COST_100
)
from main import app, bd
from models.project_model import Project
from repository.project_repository import ProjectRepository
from service.project_service import (
    get_all_projects,
    create_project,
    update_project,
    delete_project,
    project_to_dict,
    repository
)


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
            name=PROJECT_TEST,
            short_name=SHORT_NAME_TEST,
            status=STATUS_IN_PROGRESS,
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 2, 1),
            actual_end_date=None,
            cost=COST_1000,
            is_locked=False
        )
        bd.session.add(project)
        bd.session.commit()

        projects = get_all_projects()

        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['name'], PROJECT_TEST)
        self.assertEqual(projects[0]['short_name'], SHORT_NAME_TEST)
        self.assertEqual(projects[0]['status'], STATUS_IN_PROGRESS)
        self.assertEqual(projects[0]['start_date'], START_DATE_TEST)
        self.assertEqual(projects[0]['planned_end_date'], PLANNED_END_DATE)
        self.assertIsNone(projects[0]['actual_end_date'])
        self.assertEqual(projects[0]['cost'], COST_1000)

    def test_create_project(self):
        data = {
            'name': PROJECT_NEW,
            'short_name': SHORT_NAME_NEW,
            'description': DESCRIPTION_TEST,
            'planned_end_date': PLANNED_END_DATE,
            'cost': COST_2000,
            'status': STATUS_IN_PROGRESS
        }

        project = create_project(data)

        self.assertIsNotNone(project.id)
        self.assertEqual(project.name, PROJECT_NEW)
        self.assertEqual(project.short_name, SHORT_NAME_NEW)
        self.assertEqual(project.description, DESCRIPTION_TEST)
        self.assertEqual(project.planned_end_date, date(2023, 2, 1))
        self.assertIsNone(project.actual_end_date)
        self.assertEqual(project.cost, COST_2000)
        self.assertEqual(project.status, STATUS_IN_PROGRESS)

    def test_update_project(self):
        project = Project(
            name=PROJECT_TEST,
            short_name=SHORT_NAME_TEST,
            status=STATUS_IN_PROGRESS,
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 2, 1),
            actual_end_date=None,
            cost=COST_1000,
            is_locked=False
        )
        bd.session.add(project)
        bd.session.commit()

        data = {
            'name': PROJECT_UPDATED,
            'short_name': SHORT_NAME_UPDATED,
            'description': DESCRIPTION_UPDATED,
            'planned_end_date': PLANNED_END_DATE,
            'cost': COST_1500,
            'status': STATUS_COMPLETED
        }
        updated_project = update_project(project.id, data)

        self.assertEqual(updated_project.id, project.id)
        self.assertEqual(updated_project.name, PROJECT_UPDATED)
        self.assertEqual(updated_project.short_name, SHORT_NAME_UPDATED)
        self.assertEqual(updated_project.description, DESCRIPTION_UPDATED)
        self.assertEqual(updated_project.planned_end_date, date(2023, 2, 1))
        self.assertIsNone(updated_project.actual_end_date)
        self.assertEqual(updated_project.cost, COST_1500)
        self.assertEqual(updated_project.status, STATUS_COMPLETED)

    def test_delete_project(self):
        project_data = {
            'name': PROJECT_TEST,
            'short_name': SHORT_NAME_TEST,
            'description': DESCRIPTION_TEST_PROJECT,
            'start_date': date.today(),
            'planned_end_date': date.today().strftime('%Y-%m-%d'),
            'actual_end_date': None,
            'cost': COST_100,
            'status': STATUS_IN_PROGRESS
        }
        project = create_project(project_data)
        project_id = project.id

        result = delete_project(project_id)
        self.assertTrue(result)

        deleted_project = repository.get_by_id(project_id)
        self.assertIsNone(deleted_project)

    def test_project_to_dict(self):
        project = Project(
            name=PROJECT_TEST,
            short_name=SHORT_NAME_TEST,
            status=STATUS_IN_PROGRESS,
            start_date=date(2023, 1, 1),
            planned_end_date=date(2023, 2, 1),
            actual_end_date=None,
            cost=COST_1000,
            is_locked=False
        )

        project_dict = project_to_dict(project)

        self.assertEqual(project_dict['name'], PROJECT_TEST)
        self.assertEqual(project_dict['short_name'], SHORT_NAME_TEST)
        self.assertEqual(project_dict['status'], STATUS_IN_PROGRESS)
        self.assertEqual(project_dict['start_date'], START_DATE_TEST)
        self.assertEqual(project_dict['planned_end_date'], PLANNED_END_DATE)
        self.assertIsNone(project_dict['actual_end_date'])
        self.assertEqual(project_dict['cost'], COST_1000)


if __name__ == '__main__':
    unittest.main()
