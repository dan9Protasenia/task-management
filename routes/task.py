from flask import Blueprint, request, jsonify
from datetime import date
from service.task_repository import TaskRepository, Task

task = Blueprint('task', __name__)
repository = TaskRepository()

@task.route('/task', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
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

    task = Task(
        name=name,
        priority=priority,
        start_date=start_date,
        planned_end_date=planned_end_date,
        actual_end_date=actual_end_date,
        status=status
    )

    repository.create(task)

    return jsonify(message='Task created successfully')

@task.route('/edit_task/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    data = request.get_json()
    task.name = data['name']
    task.priority = data['priority']
    task.status = data['status']

    repository.update(task)

    return jsonify(message='Task updated successfully')

@task.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    repository.delete(task)

    return jsonify(message='Task deleted successfully')

