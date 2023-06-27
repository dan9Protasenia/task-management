from models import bd


class Task(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    name = bd.Column(bd.String(100), nullable=False)
    priority = bd.Column(bd.Integer, nullable=False)
    start_date = bd.Column(bd.Date, nullable=False)
    planned_end_date = bd.Column(bd.Date, nullable=False)
    actual_end_date = bd.Column(bd.Date, nullable=True)
    status = bd.Column(bd.String(20), nullable=False)
    is_locked = bd.Column(bd.Boolean, nullable=False, default=False)
    project_id = bd.Column(bd.Integer, bd.ForeignKey('project.id'))
    performers = bd.relationship('Employee', secondary='task_performers', backref=bd.backref('tasks', lazy='dynamic'))

class TaskPerformers(bd.Model):
    __tablename__ = 'task_performers'
    task_id = bd.Column(bd.Integer, bd.ForeignKey('task.id'), primary_key=True)
    employee_id = bd.Column(bd.Integer, bd.ForeignKey('employee.id'), primary_key=True)
