from datetime import date
from repository.task_repository import TaskRepository, Task

repository = TaskRepository()


def get_all_tasks():
    tasks = repository.get_all()
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
    return task_list


def create_task(data):
    name = data['name']
    priority = data['priority']
    start_date = date.today()
    planned_end_date = date.today()
    actual_end_date = None  # Исправлено: установка значения по умолчанию None
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

def update_task(task_id, data):
    task = repository.get_by_id(task_id)
    task.name = data['name']
    task.priority = data['priority']
    task.status = data['status']
    repository.update(task)

    return task

def delete_task(task_id):
    task = repository.get_by_id(task_id)
    repository.delete(task)
    return task