from repository.job_repository import JobRepository, Job

repository = JobRepository()

def get_all_jobs():
    jobs = repository.get_all()
    job_list = []
    for job in jobs:
        job_data = {
            'name_position': job.name_position,
            'tariff_rate': job.tariff_rate
        }
        job_list.append(job_data)
    return job_list

def create_job(data):
    name_position = data['name_position']
    tariff_rate = data['tariff_rate']

    job = Job(
        name_position=name_position,
        tariff_rate=tariff_rate
    )

    repository.create(job)

def update_job(job_id, data):
    job = repository.get_by_id(job_id)
    job.name_position = data['name_position']
    job.tariff_rate = data['tariff_rate']
    repository.update(job)

def delete_job(job_id):
    job = repository.get_by_id(job_id)
    repository.delete(job)