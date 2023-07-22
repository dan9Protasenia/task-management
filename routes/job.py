import logging

from flask import Blueprint, request, jsonify, render_template

from service.job_service import get_all_jobs, create_job, update_job, delete_job, get_job

job = Blueprint('job', __name__)


@job.route('/jobs', methods=['GET'])
def get_jobs():
    name_filter = request.args.get('name_filter')
    jobs = get_all_jobs(name_filter=name_filter)

    if request.headers.get('Accept') == 'application/json':
        return jsonify(jobs=jobs)
    else:
        return render_template('jobs.html', jobs=jobs)


@job.after_request
def after_request(response):
    log_message = f'{request.method} {request.path} - {response.status_code}'
    logging.info(log_message)
    return response


@job.route('/create_job', methods=['POST', "GET"])
def create_job_route():
    if request.method == "POST":
        try:
            data = request.get_json()
            create_job(data)
            return jsonify(message='Job created successfully'), 201
        except Exception as e:
            return jsonify(message='Failed to create employee: ' + str(e)), 500
    else:
        return render_template('create_job.html')


@job.route('/edit_job/<int:job_id>', methods=['PUT', 'GET'])
def edit_job_route(job_id):
    if request.method == "PUT":
        data = request.get_json()
        update_job(job_id, data)
        return jsonify(message='Job updated successfully')
    else:
        job_data = get_job(job_id)
        return render_template('edit_job.html', job=job_data)


@job.route('/delete_job/<int:job_id>', methods=['DELETE'])
def delete_job_route(job_id):
    success = delete_job(job_id)
    if success:
        return jsonify(message='Job deleted successfully')
    return jsonify(message='Job not found'), 404
