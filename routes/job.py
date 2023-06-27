import logging

from flask import Blueprint, request, jsonify

from service.job_service import get_all_jobs, create_job, update_job, delete_job

job = Blueprint('job', __name__)


@job.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = get_all_jobs()
    return jsonify(jobs=jobs)


@job.after_request
def after_request(response):
    log_message = f'{request.method} {request.path} - {response.status_code}'
    logging.info(log_message)
    return response


@job.route('/create_job', methods=['POST'])
def create_job_route():
    data = request.get_json()
    job = create_job(data)
    if job:
        job_data = {
            'name_position': job.name_position,
            'tariff_rate': job.tariff_rate,
            'assigned_employees': job.assigned_employees,
            'id': job.id
        }
        return jsonify(message='Job created successfully', job=job_data), 201
    return jsonify(message='Failed to create job'), 400


@job.route('/edit_job/<int:job_id>', methods=['PUT'])
def edit_job_route(job_id):
    data = request.get_json()
    job = update_job(job_id, data)
    if job:
        return jsonify(message='Job updated successfully', job=job)
    return jsonify(message='Job not found'), 404


@job.route('/delete_job/<int:job_id>', methods=['DELETE'])
def delete_job_route(job_id):
    success = delete_job(job_id)
    if success:
        return jsonify(message='Job deleted successfully')
    return jsonify(message='Job not found'), 404
