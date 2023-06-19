from repository.project_repository import ProjectRepository
from datetime import date, datetime
from models.project_model import Project

repository = ProjectRepository()

def get_all_projects():
    projects = repository.get_all()
    project_list = []
    for project_data in projects:
        project_dict = {
            'name': project_data.name,
            'short_name': project_data.short_name,
            'description': project_data.description,
            'start_date': project_data.start_date.strftime('%Y-%m-%d'),
            'planned_end_date': project_data.planned_end_date.strftime('%Y-%m-%d'),
            'actual_end_date': project_data.actual_end_date.strftime('%Y-%m-%d') if project_data.actual_end_date else None,
            'cost': project_data.cost,
            'status': project_data.status
        }
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
    project.status = data['status']
    project.planned_end_date = datetime.strptime(data['planned_end_date'], '%Y-%m-%d').date()

    repository.update(project)

    return project

def delete_project(project_id):
    result = repository.delete(project_id)

    return result

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
