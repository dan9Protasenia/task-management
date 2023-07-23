from datetime import date

from repository.task_repository import TaskRepository, Task

repository = TaskRepository()


def get_task(task_id):
    task = repository.get_by_id(task_id)
    if task:
        employee_dict = task_to_dict(task)
        employee_dict['id'] = task.id
        return employee_dict
    return None


def get_project_details(project_id):
    try:
        project = repository.get_by_id(project_id)

        if project:
            return project
        else:
            return None
    except Exception as e:

        print("Error getting project details:", e)
        return None


def get_all_tasks(project_id, name_filter=None, start_date_from_filter=None, start_date_to_filter=None,
                  end_date_from_filter=None, end_date_to_filter=None, overdue_filter=None,
                  cost_from_filter=None, cost_to_filter=None):
    tasks = repository.get_all()
    task_list = []
    for task in tasks:
        if name_filter and name_filter.lower() not in task.name.lower():
            continue

        if start_date_from_filter:
            start_date_from = date.fromisoformat(start_date_from_filter)
            if task.start_date < start_date_from:
                continue

        if start_date_to_filter:
            start_date_to = date.fromisoformat(start_date_to_filter)
            if task.start_date > start_date_to:
                continue

        if end_date_from_filter:
            end_date_from = date.fromisoformat(end_date_from_filter)
            if task.planned_end_date < end_date_from:
                continue

        if end_date_to_filter:
            end_date_to = date.fromisoformat(end_date_to_filter)
            if task.planned_end_date > end_date_to:
                continue

        if overdue_filter == 'true':
            if task.planned_end_date >= date.today():
                continue

        if cost_from_filter:
            cost_from = float(cost_from_filter)
            if task.cost < cost_from:
                continue

        if cost_to_filter:
            cost_to = float(cost_to_filter)
            if task.cost > cost_to:
                continue

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
    return task_list


def create_task(project_id, data):
    name = data['name']
    priority = data['priority']
    start_date = date.today()
    planned_end_date = data['planned_end_date']
    actual_end_date = None
    status = data['status']

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
    return task


def update_task(task_id, data):
    task = repository.get_by_id(task_id)
    task.name = data['name']
    task.priority = data['priority']
    task.status = data['status']
    task.actual_end_date = data['actual_end_date']  # Get the actual end date from the input data
    repository.update(task)
    return task


def delete_task(task_id):
    task = repository.get_by_id(task_id)
    repository.delete(task)
    return task


def task_to_dict(task):
    task_dict = {
        'name': task.name,
        'priority': task.priority,
        'start_date': task.start_date.strftime('%Y-%m-%d'),
        'planned_end_date': task.planned_end_date.strftime('%Y-%m-%d'),
        'actual_end_date': task.actual_end_date.strftime('%Y-%m-%d') if task.actual_end_date else None,
        'status': task.status
    }
    return task_dict


def get_task_performers(task_id):
    performers = repository.get_task_performers(task_id)
    performer_list = []
    for performer in performers:
        performer_data = {
            'id': performer.id,
            'last_name': performer.last_name,
            'first_name': performer.first_name,
            'middle_name': performer.middle_name,
            'position': performer.position
        }
        performer_list.append(performer_data)
    return performer_list


def set_task_performers(task_id, performer_ids):
    return repository.set_task_performers(task_id, performer_ids)


def is_employee_assigned_to_task(employee_id):
    task_count = Task.query.filter(Task.performers.any(id=employee_id)).count()
    return task_count > 0
