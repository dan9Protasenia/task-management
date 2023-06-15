from flask import Flask
from routes.project import project_blueprint
from models import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'

db.init_app(app)
app.register_blueprint(project_blueprint)

if __name__ == '__main__':
    app.run()
