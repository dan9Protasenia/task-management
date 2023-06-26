from datetime import date, datetime

from flask import Blueprint, request, jsonify

from repository.project_repository import ProjectRepository, Project

project = Blueprint('project', __name__)
repository = ProjectRepository()


@project.route('/')
def index():
    return jsonify(message='Welcome to the API')


@project.route('/projects', methods=['GET'])
def get_projects():
    name_filter = request.args.get('name')
    start_date_filter = request.args.get('start_date')
    end_date_filter = request.args.get('end_date')
    overdue_filter = request.args.get('overdue')

    projects = repository.get_all()
    project_list = []

    for project in projects:
        if name_filter and name_filter.lower() not in project.name.lower():
            continue

        if start_date_filter:
            try:
                start_date_filter = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            except ValueError:
                start_date_filter = None
            if start_date_filter and project.start_date < start_date_filter:
                continue

        if end_date_filter:
            try:
                end_date_filter = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            except ValueError:
                end_date_filter = None
            if end_date_filter and project.planned_end_date > end_date_filter:
                continue

        if overdue_filter == 'true' and project.planned_end_date >= date.today():
            continue

        project_data = {
            'id': project.id,
            'name': project.name,
            'short_name': project.short_name,
            'description': project.description,
            'start_date': project.start_date.strftime('%Y-%m-%d'),
            'planned_end_date': project.planned_end_date.strftime('%Y-%m-%d'),
            'actual_end_date': project.actual_end_date.strftime('%Y-%m-%d') if project.actual_end_date else None,
            'cost': project.cost,
            'status': project.status
        }
        project_list.append(project_data)

    return jsonify(projects=project_list)


@project.route('/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data['name']
    short_name = data['short_name']
    description = data['description']
    start_date = date.today()
    planned_end_date = datetime.strptime(data['planned_end_date'], '%Y-%m-%d').date()

    actual_end_date = None
    cost = float(data['cost'])
    status = data['status']

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

    repository.create(project)

    return jsonify(message='Project created successfully')


@project.route('/edit_project/<int:project_id>', methods=['PUT'])
def edit_project(project_id):
    project = repository.get_by_id(project_id)
    data = request.get_json()
    project.name = data['name']
    project.short_name = data['short_name']
    project.description = data['description']
    project.cost = float(data['cost'])
    project.status = data['status']
    project.planned_end_date = datetime.strptime(data['planned_end_date'], '%Y-%m-%d').date()

    repository.update(project)

    return jsonify(message='Project updated successfully')


@project.route('/delete_project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = repository.get_by_id(project_id)
    repository.delete(project)

    return jsonify(message='Project deleted successfully')
