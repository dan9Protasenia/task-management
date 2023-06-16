from models.job_model import bd
from models.job_model import Job
from . import AbstractRepository

class JobRepository(AbstractRepository):
    def get_all(self):
        return Job.query.all()

    def get_by_id(self, job_id):
        return Job.query.get(job_id)

    def create(self, job):
        bd.session.add(job)
        bd.session.commit()

    def update(self, job):
        bd.session.commit()

    def delete(self, job):
        bd.session.delete(job)
        bd.session.commit()
