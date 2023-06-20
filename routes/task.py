from flask import Blueprint, request, jsonify

from service.task_service import get_all_tasks, create_task, update_task, delete_task

task = Blueprint('task', __name__)


@task.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks=tasks)


@task.route('/create_task', methods=['POST'])
def create_task_route():
    data = request.get_json()
    create_task(data)
    return jsonify(message='Task created successfully')


@task.route('/edit_task/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    update_task(task_id, data)
    return jsonify(message='Task updated successfully')


@task.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify(message='Task deleted successfully')
