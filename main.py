import logging
import sqlalchemy
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy_utils import create_database
from models.project_model import bd
from routes.employee import employee
from routes.job import job
from routes.project import project
from routes.task import task

app = Flask(__name__)


database_uri = 'sqlite:///C:/Users/Komp/PycharmProjects/qulix/instance/database.db'

# Создание новой базы данных
create_database(database_uri)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
  # Опционально, для отключения предупреждений

bd.init_app(app)

migrate = Migrate(app, bd)
logging.basicConfig(filename='app.log', level=logging.DEBUG)

app.register_blueprint(project)
app.register_blueprint(task)
app.register_blueprint(employee)
app.register_blueprint(job)

if __name__ == '__main__':
    app.run()
