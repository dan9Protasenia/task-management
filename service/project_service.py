from datetime import date, datetime

from models.project_model import Project
from repository.project_repository import ProjectRepository
from repository.task_repository import TaskRepository
from service.task_service import task_to_dict

task_repository = TaskRepository()
repository = ProjectRepository()


def get_project(project_id):
    project = repository.get_by_id(project_id)
    if project:
        project_dict = project_to_dict(project)
        project_dict['id'] = project.id
        return project_dict
    return None


def get_all_projects(name_filter=None, start_date_filter=None, end_date_filter=None, overdue_filter=None):
    projects = repository.get_all()
    project_list = []

    for project_data in projects:
        if name_filter is not None and isinstance(name_filter,
                                                  str) and name_filter.lower() not in project_data.name.lower():
            continue

        if start_date_filter:
            try:
                start_date_filter_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            except ValueError:
                start_date_filter_date = None
            if start_date_filter_date and project_data.start_date < start_date_filter_date:
                continue

        if end_date_filter:
            try:
                end_date_filter_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            except ValueError:
                end_date_filter_date = None
            if end_date_filter_date and project_data.planned_end_date > end_date_filter_date:
                continue

        if overdue_filter == 'true' and project_data.planned_end_date >= date.today():
            continue

        project_dict = project_to_dict(project_data)
        project_dict['id'] = project_data.id
        project_list.append(project_dict)

    return project_list


def create_project(data):
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

    return project


def update_project(project_id, data):
    project = repository.get_by_id(project_id)

    project.name = data['name']
    project.short_name = data['short_name']
    project.description = data['description']
    project.cost = float(data['cost'])

    if project.status != 'Завершено' and data['status'] == 'Завершено':
        project.status = 'Завершено'
        project.actual_end_date = datetime.now().date()
    else:
        project.status = data['status']

    project.planned_end_date = datetime.strptime(data['planned_end_date'], '%Y-%m-%d').date()

    repository.update(project)

    return project


def delete_project(project_id):
    project = repository.get_by_id(project_id)
    if project:
        repository.delete(project)
        return project
    return False


def project_to_dict(project):
    project_dict = {
        'name': project.name,
        'short_name': project.short_name,
        'description': project.description,
        'start_date': project.start_date.strftime('%Y-%m-%d'),
        'planned_end_date': project.planned_end_date.strftime('%Y-%m-%d'),
        'actual_end_date': project.actual_end_date.strftime('%Y-%m-%d') if project.actual_end_date else None,
        'cost': project.cost,
        'status': project.status
    }
    return project_dict


def get_project_tasks(project_id):
    tasks = task_repository.get_all_tasks_by_project(project_id)
    task_list = []
    for task in tasks:
        task_data = task_to_dict(task)
        task_list.append(task_data)
    return task_list
