from models.task_model import bd
from models.task_model import Task
from . import AbstractRepository

class TaskRepository(AbstractRepository):
    def get_all(self):
        return Task.query.all()

    def get_by_id(self, task_id):
        return Task.query.get(task_id)

    def create(self, task):
        bd.session.add(task)
        bd.session.commit()

    def update(self, task):
        bd.session.commit()

    def delete(self, task):
        bd.session.delete(task)
        bd.session.commit()
