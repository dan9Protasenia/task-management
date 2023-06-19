import unittest
from flask import Flask
from flask.testing import FlaskClient
from routes.project import project
from flask_sqlalchemy import SQLAlchemy
from models.project_model import Project
from models import bd
from main import app

class ProjectRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()
        self.app_context.pop()

    def test_create_project(self):
        project_data = {
            'name': 'Test Project',
            'short_name': 'TP',
            'description': 'This is a test project',
            'planned_end_date': '2023-06-30',
            'cost': 1000.0,
            'status': 'In Progress'
        }
        response = self.app.post('/create_project', json=project_data)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Project created successfully')

        with self.app_context:
            saved_project = Project.query.first()

            self.assertEqual(saved_project.name, 'Test Project')
            self.assertEqual(saved_project.short_name, 'TP')
            self.assertEqual(saved_project.description, 'This is a test project')
            self.assertEqual(saved_project.planned_end_date, '2023-06-30')
            self.assertEqual(saved_project.cost, 1000.0)
            self.assertEqual(saved_project.status, 'In Progress')


if __name__ == '__main__':
    unittest.main()
