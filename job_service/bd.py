from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy()

class Job(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    name_position = bd.Column(bd.String(50), nullable=False)
    tariff_rate = bd.Column(bd.Integer, nullable=False)