from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta, datetime
from models.Project import db, Project
from service.project_repository import ProjectRepository
from flask import Blueprint

project_blueprint = Blueprint('project', __name__)

project_repository = ProjectRepository()

@project_blueprint.route('/')
def index():
    return render_template('index.html')

@project_blueprint.route('/projects')
def projects():
    projects = project_repository.get_all()
    return render_template('projects.html', projects=projects, today=date.today(), timedelta=timedelta)

@project_blueprint.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        short_name = request.form['short_name']
        description = request.form['description']
        start_date = date.today()
        planned_end_date_str = request.form['planned_end_date']
        planned_end_date = datetime.strptime(planned_end_date_str, '%Y-%m-%d').date()

        actual_end_date = None
        cost = float(request.form['cost'])
        status = request.form['status']

        if status == 'Завершено':
            actual_end_date = date.today()

        project = Project(
            name=name,
            short_name=short_name,
            description=description,
            start_date=start_date,
            planned_end_date=planned_end_date,
            actual_end_date=actual_end_date,
            cost=cost,
            status=status
        )

        project_repository.create(project)

        return redirect(url_for('project.projects'))

    return render_template('create_project.html')


@project_blueprint.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = project_repository.get_by_id(project_id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.short_name = request.form['short_name']
        project.description = request.form['description']
        project.cost = float(request.form['cost'])
        project.status = request.form['status']
        project.planned_end_date = datetime.strptime(request.form['planned_end_date'], '%Y-%m-%d').date()

        project_repository.commit()

        return redirect(url_for('project.projects'))

    return render_template('edit_project.html', project=project)


@project_blueprint.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = project_repository.get_by_id(project_id)
    project_repository.delete(project)

    return redirect(url_for('project.projects'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db.init_app(app)
app.register_blueprint(project_blueprint)

if __name__ == '__main__':
    app.run()
