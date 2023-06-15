from models.Project import Project
from models import db

class ProjectRepository:
    def get_all(self):
        return Project.query.all()

    def get_by_id(self, project_id):
        return Project.query.get(project_id)

    def create(self, project):
        db.session.add(project)
        self.commit()

    def update(self):
        self.commit()

    def delete(self, project):
        db.session.delete(project)
        self.commit()

    def commit(self):
        db.session.commit()
