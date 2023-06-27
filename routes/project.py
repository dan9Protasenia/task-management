from flask import Blueprint, request, jsonify

from service.project_service import (
    get_all_projects,
    create_project,
    update_project,
    delete_project,
    get_project_tasks,
)

project = Blueprint('project', __name__)


@project.route('/')
def index():
    return jsonify(message='Welcome to the API')


@project.route('/projects', methods=['GET'])
def get_projects():
    name_filter = request.args.get('name')
    start_date_filter = request.args.get('start_date')
    end_date_filter = request.args.get('end_date')
    overdue_filter = request.args.get('overdue')

    projects = get_all_projects(name_filter=name_filter, start_date_filter=start_date_filter,
                                end_date_filter=end_date_filter, overdue_filter=overdue_filter)

    return jsonify(projects=projects)


@project.route('/create_project', methods=['POST'])
def create_project_route():
    data = request.get_json()
    create_project(data)
    return jsonify(message='Project created successfully')


@project.route('/edit_project/<int:project_id>', methods=['PUT'])
def edit_project(project_id):
    data = request.get_json()
    update_project(project_id, data)
    return jsonify(message='Project updated successfully')


@project.route('/delete_project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = delete_project(project_id)
    if project:
        return jsonify(message='Project deleted successfully')
    return jsonify(message='Project not found')


@project.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks_route(project_id):
    return jsonify(tasks=get_project_tasks(project_id))
