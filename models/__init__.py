from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy()

from .project_model import Project
from .task_model import Task
from .employee_model import Employee
from .job_model import Job
