from models.job_model import Job
from models.job_model import bd
from . import AbstractRepository


class JobRepository(AbstractRepository):
    def get_all(self):
        return Job.query.filter_by(is_locked=False).all()

    def get_by_id(self, project_id):
        return Job.query.filter_by(id=project_id, is_locked=False).first()

    def create(self, project):
        bd.session.add(project)
        bd.session.commit()

    def update(self, project):
        bd.session.commit()

    def delete(self, project):
        bd.session.delete(project)
        bd.session.commit()

    def get_employees(self, job_id):
        job = self.get_by_id(job_id)
        if job:
            return job.employees
        return []
