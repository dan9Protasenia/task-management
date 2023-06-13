from flask import Flask, render_template, request, redirect, url_for

from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

project = Flask(__name__)
project.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(project)
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    planned_end_date = db.Column(db.Date, nullable=False)
    actual_end_date = db.Column(db.Date, nullable=True)

@project.route('/')
def index():
    return render_template('index.html')

@project.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@project.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        short_name = request.form['short_name']
        description = request.form['description']
        start_date = date.today()
        planned_end_date = date.today()
        actual_end_date = date.today()

        project = Project(
            name=name,
            short_name=short_name,
            description=description,
            start_date=start_date,
            planned_end_date=planned_end_date,
            actual_end_date=actual_end_date
        )

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('projects'))

    return render_template('create_project.html')

@project.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get(project_id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.short_name = request.form['short_name']
        project.description = request.form['description']

        db.session.commit()

        return redirect(url_for('projects'))

    return render_template('edit_project.html', project=project)

@project.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('projects'))

# def clear_database():
#     with app.app_context():
#         db.session.query(Project).delete()
#         db.session.commit()

if __name__ == '__main__':
    # clear_database()
    # project.run(port=5000)
    project.run()
