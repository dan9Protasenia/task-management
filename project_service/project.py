from flask import Flask, render_template, request, redirect, url_for

from datetime import date, timedelta, datetime
from bd import bd, Project

project = Flask(__name__)
project.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
# project.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bd.init_app(project)

@project.route('/')
def index():
    return render_template('index.html')

@project.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects, today=date.today(), timedelta=timedelta)

@project.route('/create_project', methods=['GET', 'POST'])
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

        bd.session.add(project)
        bd.session.commit()

        return redirect(url_for('projects'))

    return render_template('create_project.html')


@project.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get(project_id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.short_name = request.form['short_name']
        project.description = request.form['description']
        project.cost = float(request.form['cost'])
        project.status = request.form['status']
        project.planned_end_date = datetime.strptime(request.form['planned_end_date'], '%Y-%m-%d').date()

        bd.session.commit()

        return redirect(url_for('projects'))

    return render_template('edit_project.html', project=project)


@project.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    bd.session.delete(project)
    bd.session.commit()

    return redirect(url_for('projects'))

# def clear_database():
#     with app.app_context():
#         db.session.query(Project).delete()
#         db.session.commit()

if __name__ == '__main__':
    # clear_database()
    # project.run(port=5000)
    project.run()
