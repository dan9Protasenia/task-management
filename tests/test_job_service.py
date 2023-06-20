import unittest

from main import app, bd
from models.job_model import Job
from repository.job_repository import JobRepository
from service.job_service import get_all_jobs, create_job, update_job, delete_job


class JobServiceTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()
        self.client = app.test_client()
        self.repository = JobRepository()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()

    def test_get_all_jobs(self):
        job1 = Job(name_position='Job 1', tariff_rate=10.0)
        job2 = Job(name_position='Job 2', tariff_rate=20.0)
        job3 = Job(name_position='Job 3', tariff_rate=9999999999990.0)
        job4 = Job(name_position='Job 4', tariff_rate=0.0)
        self.repository.create(job1)
        self.repository.create(job2)
        self.repository.create(job3)
        self.repository.create(job4)

        jobs = get_all_jobs()

        self.assertEqual(len(jobs), 4)
        self.assertEqual(jobs[0]['name_position'], 'Job 1')
        self.assertEqual(jobs[0]['tariff_rate'], 10.0)
        self.assertEqual(jobs[1]['name_position'], 'Job 2')
        self.assertEqual(jobs[1]['tariff_rate'], 20.0)
        self.assertEqual(jobs[2]['name_position'], 'Job 3')
        self.assertEqual(jobs[2]['tariff_rate'], 9999999999990.0)
        self.assertEqual(jobs[3]['name_position'], 'Job 4')
        self.assertEqual(jobs[3]['tariff_rate'], 0.0)

    def test_create_job(self):
        data = {
            'name_position': 'New Job',
            'tariff_rate': 15.0
        }

        jobs = create_job(data)

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].name_position, 'New Job')
        self.assertEqual(jobs[0].tariff_rate, 15.0)

    def test_update_job(self):
        job = Job(name_position='Job 1', tariff_rate=10.0)
        self.repository.create(job)

        data = {
            'name_position': 'Updated Job',
            'tariff_rate': 20.0
        }

        updated_job = update_job(job.id, data)

        self.assertEqual(updated_job.name_position, 'Updated Job')
        self.assertEqual(updated_job.tariff_rate, 20.0)

    def test_delete_job(self):
        job_data = {
            'name_position': 'Test Job',
            'tariff_rate': 10.0
        }
        job = create_job(job_data)
        job_id = job[0].id

        result = delete_job(job_id)
        self.assertTrue(result)

        deleted_job = self.repository.get_by_id(job_id)
        self.assertIsNone(deleted_job)


if __name__ == '__main__':
    unittest.main()
