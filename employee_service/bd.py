from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy()

class Employee(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    last_name = bd.Column(bd.String(50), nullable=False)
    first_name = bd.Column(bd.String(50), nullable=False)
    middle_name = bd.Column(bd.String(50), nullable=True)
    position = bd.Column(bd.String(100), nullable=False)