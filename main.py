import logging

from flask import Flask
from flask_migrate import Migrate

from models.project_model import bd
from routes.employee import employee
from routes.job import job
from routes.project import project
from routes.task import task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Komp/PycharmProjects/qulix/instance/database.db'
bd.init_app(app)

migrate = Migrate(app, bd)
logging.basicConfig(filename='app.log', level=logging.DEBUG)

app.register_blueprint(project)
app.register_blueprint(task)
app.register_blueprint(employee)
app.register_blueprint(job)

if __name__ == '__main__':
    app.run()
