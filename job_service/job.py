from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

job = Flask(__name__)
job.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'

db = SQLAlchemy(job)
migrate = Migrate(job, db)
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_position = db.Column(db.String(50), nullable=False)
    tariff_rate = db.Column(db.Integer, nullable=False)
@job.before_request
def create_tables():
    db.create_all()
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

        db.session.add(job)
        db.session.commit()

        return redirect(url_for('jobs'))

    return render_template('create_job.html')

@job.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get(job_id)

    if request.method == 'POST':
        job.name_position = request.form['name_position']
        job.tariff_rate = request.form['tariff_rate']

        db.session.commit()

        return redirect(url_for('jobs'))

    return render_template('edit_job.html', job=job)

@job.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    db.session.delete(job)
    db.session.commit()

    return redirect(url_for('jobs'))

if __name__ == '__main__':
    job.run(port=5005)
