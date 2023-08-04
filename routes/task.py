import logging

from flask import Blueprint, request, jsonify, render_template

from service.task_service import (
    create_task,
    update_task,
    delete_task,
    get_task_performers,
    get_task,
    get_all_tasks,
    get_project_details
)

task = Blueprint('task', __name__)


@task.route('/tasks/<int:project_id>', methods=['GET'])
def get_tasks(project_id):
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    project = get_project_details(project_id)

    logging.debug("Entering get_tasks function")


        # return jsonify(message="Project not found"), 404

    name_filter = request.args.get('name')
    start_date_from_filter = request.args.get('start_date')
    start_date_to_filter = request.args.get('start_date')
    end_date_from_filter = request.args.get('planned_end_date')
    end_date_to_filter = request.args.get('planned_end_date')
    overdue_filter = request.args.get('planned_end_date')
    cost_from_filter = request.args.get('cost')
    cost_to_filter = request.args.get('cost')

    logging.debug(f"Parameters: name_filter={name_filter}, "
                  f"start_date_from_filter={start_date_from_filter}, "
                  f"start_date_to_filter={start_date_to_filter}, "
                  f"end_date_from_filter={end_date_from_filter}, "
                  f"end_date_to_filter={end_date_to_filter}, "
                  f"overdue_filter={overdue_filter}, "
                  f"cost_from_filter={cost_from_filter}, "
                  f"cost_to_filter={cost_to_filter}")

    tasks = get_all_tasks(project_id=project_id,
                          name_filter=name_filter,
                          start_date_from_filter=start_date_from_filter,
                          start_date_to_filter=start_date_to_filter,
                          end_date_from_filter=end_date_from_filter,
                          end_date_to_filter=end_date_to_filter,
                          overdue_filter=overdue_filter,
                          cost_from_filter=cost_from_filter,
                          cost_to_filter=cost_to_filter
                          )

    logging.debug(f"Tasks: {tasks}")
    if project is None:
        return render_template('tasks.html', tasks=tasks, project_id=project_id, project=project)
    if request.headers.get('Accept') == 'application/json':
        return jsonify(tasks=tasks)
    else:
        return render_template('tasks.html', tasks=tasks, project_id=project_id, project=project)


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


@task.route('/edit_task/<int:project_id>/<int:task_id>', methods=['PUT', 'GET'])
def edit_task_route(project_id, task_id):
    if request.method == "PUT":
        data = request.get_json()
        update_task(task_id, data)
        return jsonify(message="Task updated successfully")
    else:
        task_data = get_task(task_id)
        return render_template('edit_task.html', task=task_data, project_id=project_id)


@task.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify(message='Task deleted successfully')


@task.route('/task_performers/<int:task_id>', methods=['GET'])
def get_performers(task_id):
    performers = get_task_performers(task_id)
    return jsonify(performers), 200
