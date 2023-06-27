from models import bd


class Job(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    name_position = bd.Column(bd.String(50), nullable=False)
    tariff_rate = bd.Column(bd.Integer, nullable=False)
    is_locked = bd.Column(bd.Boolean, nullable=False, default=False)
    employees = bd.relationship('Employee', backref='job', lazy=True)
