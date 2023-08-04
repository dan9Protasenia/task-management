import unittest

from constants import (
    NAME_JOB_1,
    NAME_JOB_2,
    NAME_JOB_3,
    NAME_JOB_4,
    NAME_NEW_JOB,
    NAME_UPDATED_JOB,
    NAME_TEST_JOB,
    TARIFF_RATE_10,
    TARIFF_RATE_20,
    TARIFF_RATE_9999999999990,
    TARIFF_RATE_0,
    TARIFF_RATE_15
)
from main import app, bd
from models.job_model import Job
from repository.job_repository import JobRepository
from service.job_service import get_all_jobs, create_job, update_job, delete_job


class JobServiceTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        bd.create_all()
        self.client = app.test_client()
        self.repository = JobRepository()

    def tearDown(self):
        bd.session.remove()
        bd.drop_all()

    def test_get_all_jobs(self):
        job1 = Job(name_position=NAME_JOB_1, tariff_rate=TARIFF_RATE_10)
        job2 = Job(name_position=NAME_JOB_2, tariff_rate=TARIFF_RATE_20)
        job3 = Job(name_position=NAME_JOB_3, tariff_rate=TARIFF_RATE_9999999999990)
        job4 = Job(name_position=NAME_JOB_4, tariff_rate=TARIFF_RATE_0)
        self.repository.create(job1)
        self.repository.create(job2)
        self.repository.create(job3)
        self.repository.create(job4)

        jobs = get_all_jobs()

        self.assertEqual(len(jobs), 4)
        self.assertEqual(jobs[0]['name_position'], NAME_JOB_1)
        self.assertEqual(jobs[0]['tariff_rate'], TARIFF_RATE_10)
        self.assertEqual(jobs[1]['name_position'], NAME_JOB_2)
        self.assertEqual(jobs[1]['tariff_rate'], TARIFF_RATE_20)
        self.assertEqual(jobs[2]['name_position'], NAME_JOB_3)
        self.assertEqual(jobs[2]['tariff_rate'], TARIFF_RATE_9999999999990)
        self.assertEqual(jobs[3]['name_position'], NAME_JOB_4)
        self.assertEqual(jobs[3]['tariff_rate'], TARIFF_RATE_0)

    def test_create_job(self):
        data = {
            'name_position': NAME_NEW_JOB,
            'tariff_rate': TARIFF_RATE_15
        }

        job = create_job(data)

        self.assertIsInstance(job, Job)
        self.assertEqual(job.name_position, NAME_NEW_JOB)
        self.assertEqual(job.tariff_rate, TARIFF_RATE_15)

    def test_update_job(self):
        job = Job(name_position=NAME_JOB_1, tariff_rate=TARIFF_RATE_10)
        self.repository.create(job)

        data = {
            'name_position': NAME_UPDATED_JOB,
            'tariff_rate': TARIFF_RATE_20
        }

        updated_job = update_job(job.id, data)

        self.assertEqual(updated_job.name_position, NAME_UPDATED_JOB)
        self.assertEqual(updated_job.tariff_rate, TARIFF_RATE_20)

    def test_delete_job(self):
        job_data = {
            'name_position': NAME_TEST_JOB,
            'tariff_rate': TARIFF_RATE_10
        }
        job = create_job(job_data)
        job_id = job.id

        result = delete_job(job_id)
        self.assertTrue(result)

        deleted_job = self.repository.get_by_id(job_id)
        self.assertIsNone(deleted_job)


if __name__ == '__main__':
    unittest.main()
