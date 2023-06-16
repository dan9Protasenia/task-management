from flask import Blueprint, request, jsonify
from service.job_repository import JobRepository, Job

job = Blueprint('job', __name__)
repository = JobRepository()

@job.route('/job', methods=['GET'])
def jobs():
    jobs = repository.get_all()
    job_list = []
    for job in jobs:
        job_data = {
            'name': job.name,
            'tariff_rate': job.tariff_rate
        }
        job_list.append(job_data)
    return jsonify(jobs=job_list)


@job.route('/create_job', methods=['POST'])
def create_job():
    data = request.get_json()
    name_position = data['name_position']
    tariff_rate = data['tariff_rate']

    job = Job(
        name_position=name_position,
        tariff_rate=tariff_rate
    )

    job_repository.create(job)

    return jsonify(message='Job created successfully')


@job.route('/edit_job/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    job = repository.get_by_id(job_id)

    data = request.get_json()
    job.name_position = data['name_position']
    job.tariff_rate = data['tariff_rate']

    repository.update(job)

    return jsonify(message='Job updated successfully')


@job.route('/delete_job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = repository.get_by_id(job_id)
    repository.delete(job)

    return jsonify(message='Job deleted successfully')


