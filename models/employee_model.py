from models import bd


class Employee(bd.Model):
    __tablename__ = 'employee'
    id = bd.Column(bd.Integer, primary_key=True)
    last_name = bd.Column(bd.String(50), nullable=False)
    first_name = bd.Column(bd.String(50), nullable=False)
    middle_name = bd.Column(bd.String(50), nullable=True)
    position = bd.Column(bd.String(100), nullable=False)
    is_locked = bd.Column(bd.Boolean, nullable=False, default=False)
    job_id = bd.Column(bd.Integer, bd.ForeignKey('job.id'), nullable=True)

    job = bd.relationship('Job', lazy=True)

