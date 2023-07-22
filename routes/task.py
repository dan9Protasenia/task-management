from datetime import date

from flask import Blueprint, request, jsonify, render_template

from repository.task_repository import Task
from service.task_service import create_task, update_task, delete_task, get_task_performers, set_task_performers, get_task

task = Blueprint('task', __name__)


@task.route('/tasks/<int:project_id>', methods=['GET'])
def get_tasks(project_id):
    name_filter = request.args.get('name')
    start_date_from_filter = request.args.get('start_date_from')
    start_date_to_filter = request.args.get('start_date_to')
    end_date_from_filter = request.args.get('end_date_from')
    end_date_to_filter = request.args.get('end_date_to')
    overdue_filter = request.args.get('overdue')
    cost_from_filter = request.args.get('cost_from')
    cost_to_filter = request.args.get('cost_to')

    tasks_query = Task.query.filter_by(project_id=project_id)

    if name_filter:
        tasks_query = tasks_query.filter(Task.name.ilike(f'%{name_filter}%'))

    if start_date_from_filter:
        start_date_from = date.fromisoformat(start_date_from_filter)
        tasks_query = tasks_query.filter(Task.start_date >= start_date_from)

    if start_date_to_filter:
        start_date_to = date.fromisoformat(start_date_to_filter)
        tasks_query = tasks_query.filter(Task.start_date <= start_date_to)

    if end_date_from_filter:
        end_date_from = date.fromisoformat(end_date_from_filter)
        tasks_query = tasks_query.filter(Task.planned_end_date >= end_date_from)

    if end_date_to_filter:
        end_date_to = date.fromisoformat(end_date_to_filter)
        tasks_query = tasks_query.filter(Task.planned_end_date <= end_date_to)

    if overdue_filter == 'true':
        tasks_query = tasks_query.filter(Task.planned_end_date < date.today())

    if cost_from_filter:
        cost_from = float(cost_from_filter)
        tasks_query = tasks_query.filter(Task.cost >= cost_from)

    if cost_to_filter:
        cost_to = float(cost_to_filter)
        tasks_query = tasks_query.filter(Task.cost <= cost_to)

    tasks = tasks_query.all()

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

    if request.headers.get('Accept') == 'application/json':
        return jsonify(tasks=tasks)
    else:
        return render_template('tasks.html', tasks=tasks, project_id=project_id)


@task.route('/create_task/<int:project_id>', methods=['POST', 'GET'])
def create_task_route(project_id):
    if request.method == "POST":
        try:
            data = request.get_json()
            task = create_task(project_id, data)
            return jsonify(message='Task created successfully', task_id=task.id), 201
        except Exception as e:
            return jsonify(message='Failed to create task: ' + str(e)), 500
    else:
        return render_template('create_task.html', project_id=project_id)


@task.route('/edit_task/<int:task_id>', methods=['PUT', 'GET'])
def edit_task_route(task_id):
    if request.method == "PUT":
        data = request.get_json()
        update_task(task_id, data)
        return jsonify(message="Task updated successfully")
    else:
        task_data = get_task(task_id)
        return render_template('edit_task.html', task=task_data)


@task.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify(message='Task deleted successfully')


@task.route('/task_performers/<int:task_id>', methods=['GET'])
def get_performers(task_id):
    performers = get_task_performers(task_id)
    return jsonify(performers), 200


@task.route('/task_performers/<int:task_id>', methods=['POST'])
def set_performers(task_id):
    data = request.get_json()
    performer_ids = data.get('performer_ids', [])
    if set_task_performers(task_id, performer_ids):
        return jsonify({'message': 'Performers updated successfully'}), 200
    return jsonify({'message': 'Failed to update performers'}), 400


@task.route('/task_performers/<int:task_id>/<int:performer_id>', methods=['DELETE'])
def delete_performers(task_id, performer_id):
    performers = get_task_performers(task_id)
    if not performers:
        return jsonify(message='Performers not found'), 404

    performer_id = int(performer_id)
    if performer_id in performers:
        performers.remove(performer_id)
        if set_task_performers(task_id, performers):
            return jsonify(message='Performer deleted successfully'), 200

    return jsonify(message='Failed to delete performer'), 400
