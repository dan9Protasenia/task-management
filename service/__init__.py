from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .project_repository import ProjectRepository
from .task_repository import TaskRepository
from .employee_repository import EmployeeRepository
from .job_repository import JobRepository

project_repository = ProjectRepository()
task_repository = TaskRepository()
employee_repository = EmployeeRepository()
job_repository = JobRepository()
