from flask import Flask, render_template, request, redirect, url_for
from bd import bd, Job

job = Flask(__name__)
job.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'

bd.init_app(job)

@job.route('/job')
def jobs():
    jobs = Job.query.all()
    return render_template('job.html', jobs=jobs)

@job.route('/create_job', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        name_position = request.form['name_position']
        tariff_rate = request.form['tariff_rate']

        job = Job(
            name_position=name_position,
            tariff_rate=tariff_rate
        )

        bd.session.add(job)
        bd.session.commit()

        return redirect(url_for('jobs'))

    return render_template('create_job.html')

@job.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get(job_id)

    if request.method == 'POST':
        job.name_position = request.form['name_position']
        job.tariff_rate = request.form['tariff_rate']

        bd.session.commit()

        return redirect(url_for('jobs'))

    return render_template('edit_job.html', job=job)

@job.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    bd.session.delete(job)
    bd.session.commit()

    return redirect(url_for('jobs'))

if __name__ == '__main__':
    job.run(port=5005)
