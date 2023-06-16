from models import bd


class Project(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    name = bd.Column(bd.String(100), nullable=False)
    short_name = bd.Column(bd.String(20), nullable=False)
    status = bd.Column(bd.String(20), nullable=False)
    description = bd.Column(bd.Text, nullable=True)
    start_date = bd.Column(bd.Date, nullable=False)
    planned_end_date = bd.Column(bd.Date, nullable=False)
    actual_end_date = bd.Column(bd.Date, nullable=True)
    cost = bd.Column(bd.Float, nullable=False)
