from flask import Blueprint

project_blueprint = Blueprint('project', __name__)
task_blueprint = Blueprint('task', __name__)
job_blueprint = Blueprint('job', __name__)
employee_blueprint = Blueprint('employee', __name__)

from . import project
from . import task
from . import employee
from . import job