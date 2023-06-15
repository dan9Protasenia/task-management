from . import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    planned_end_date = db.Column(db.Date, nullable=False)
    actual_end_date = db.Column(db.Date, nullable=True)
    cost = db.Column(db.Float, nullable=False)

