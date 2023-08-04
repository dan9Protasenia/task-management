from repository.job_repository import JobRepository, Job

repository = JobRepository()


def get_job(job_id):
    job = repository.get_by_id(job_id)
    if job:
        job_dict = job_to_dict(job)
        job_dict['id'] = job.id
        return job_dict
    return None


def get_all_jobs(name_filter=None):
    jobs = repository.get_all()
    job_list = []

    for job in jobs:
        job_dict = job_to_dict(job)

        if name_filter is not None and isinstance(name_filter, str):
            if name_filter.lower() not in job_dict['name_position'].lower() \
                    and name_filter.lower() not in str(job_dict['tariff_rate']).lower():
                continue

        job_dict['id'] = job.id
        job_list.append(job_dict)

    return job_list



def create_job(data):
    name_position = data['name_position']
    tariff_rate = data['tariff_rate']

    job = Job(
        name_position=name_position,
        tariff_rate=tariff_rate
    )

    repository.create(job)
    # job.assigned_employees = get_assigned_employees(job.id)
    return job


def update_job(job_id, data):
    job = repository.get_by_id(job_id)
    job.name_position = data['name_position']
    job.tariff_rate = data['tariff_rate']
    repository.update(job)
    return job


def delete_job(job_id):
    job = repository.get_by_id(job_id)
    if job:
        repository.delete(job)
        return True
    return False


def job_to_dict(job):
    job_dict = {
        'name_position': job.name_position,
        'tariff_rate': job.tariff_rate,
        # 'assigned_employees': job.assigned_employees,
        # Add other fields as needed
    }
    return job_dict
