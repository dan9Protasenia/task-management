from datetime import date

from flask import Blueprint, request, jsonify

from repository.task_repository import TaskRepository, Task

task = Blueprint('task', __name__)
repository = TaskRepository()


@task.route('/tasks/<int:project_id>', methods=['GET'])
def get_tasks(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'start_date': task.start_date.strftime('%Y-%m-%d'),
            'planned_end_date': task.planned_end_date.strftime('%Y-%m-%d'),
            'actual_end_date': task.actual_end_date.strftime('%Y-%m-%d') if task.actual_end_date else None,
            'status': task.status
        }
        task_list.append(task_data)
    return jsonify(tasks=task_list)


@task.route('/create_task', methods=['POST'])
def create_task():
    data = request.get_json()
    name = data['name']
    priority = data['priority']
    start_date = date.today()
    planned_end_date = date.today()
    actual_end_date = date.today()
    status = data['status']
    project_id = data['project_id']

    task = Task(
        name=name,
        priority=priority,
        start_date=start_date,
        planned_end_date=planned_end_date,
        actual_end_date=actual_end_date,
        status=status,
        project_id=project_id
    )

    repository.create(task)

    return jsonify(message='Task created successfully')


@task.route('/edit_task/<int:project_id>/<int:task_id>', methods=['PUT'])
def edit_task(project_id, task_id):
    task = Task.query.filter_by(project_id=project_id, id=task_id).first()
    if task is None:
        return jsonify(message='Task not found'), 404

    data = request.get_json()
    task.name = data.get('name', task.name)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)

    repository.update(task)

    return jsonify(message='Task updated successfully')


@task.route('/delete_task/<int:project_id>/<int:task_id>', methods=['DELETE'])
def delete_task(project_id, task_id):
    task = Task.query.filter_by(project_id=project_id, id=task_id).first()
    if task is None:
        return jsonify(message='Task not found'), 404

    repository.delete(task)

    return jsonify(message='Task deleted successfully')
