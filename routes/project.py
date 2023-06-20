from flask import Blueprint, request, jsonify

from service.project_service import get_all_projects, create_project, update_project, delete_project, project_to_dict

project = Blueprint('project', __name__)


@project.route('/')
def index():
    return jsonify(message='Welcome to the API')


@project.route('/projects', methods=['GET'])
def get_projects():
    projects = get_all_projects()
    return jsonify(projects=projects)


@project.route('/create_project', methods=['POST'])
def create_project_route():
    data = request.get_json()
    project = create_project(data)
    if project:
        project_dict = project_to_dict(project)
        return jsonify(message='Проект успешно создан', project=project_dict)
    else:
        return jsonify(message='Не удалось создать проект'), 400


@project.route('/edit_project/<int:project_id>', methods=['PUT'])
def edit_project(project_id):
    data = request.get_json()
    project = update_project(project_id, data)
    if project:
        project_dict = project_to_dict(project)
        return jsonify(message='Проект успешно обновлен', project=project_dict)
    else:
        return jsonify(message='Не удалось обновить проект'), 400


@project.route('/delete_project/<int:project_id>', methods=['DELETE'])
def delete_project_route(project_id):
    result = delete_project(project_id)
    if result:
        return jsonify(message='Проект успешно удален')
    else:
        return jsonify(message='Не удалось удалить проект'), 400
