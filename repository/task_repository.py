from models.task_model import Task
from models.task_model import bd
from . import AbstractRepository


class TaskRepository(AbstractRepository):
    def get_all(self):
        return Task.query.filter_by(is_locked=False).all()

    def get_all_tasks_by_project(self, project_id):
        return Task.query.filter_by(project_id=project_id, is_locked=False).all()

    def get_all_tasks_by_project(self, project_id):
        return Task.query.filter_by(project_id=project_id, is_locked=False).all()

    def get_by_id(self, task_id):
        return Task.query.filter_by(id=task_id, is_locked=False).first()

    def create(self, task):
        bd.session.add(task)
        bd.session.commit()

    def update(self, task):
        bd.session.commit()

    def delete(self, task):
        if task:
            bd.session.delete(task)
            bd.session.commit()
            return True
        return False
