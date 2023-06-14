from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy()

class Task(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    name = bd.Column(bd.String(100), nullable=False)
    priority = bd.Column(bd.Integer, nullable=False)
    start_date = bd.Column(bd.Date, nullable=False)
    planned_end_date = bd.Column(bd.Date, nullable=False)
    actual_end_date = bd.Column(bd.Date, nullable=True)
    status = bd.Column(bd.String(20), nullable=False)