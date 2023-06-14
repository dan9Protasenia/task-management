from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from bd import bd, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'

bd.init_app(app)

@app.route('/task')
def task():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        name = request.form['name']
        priority = request.form['priority']
        start_date = date.today()
        planned_end_date = date.today()
        actual_end_date = date.today()
        status = request.form['status']

        task = Task(
            name=name,
            priority=priority,
            start_date=start_date,
            planned_end_date=planned_end_date,
            actual_end_date=actual_end_date,
            status=status
        )

        bd.session.add(task)
        bd.session.commit()

        return redirect(url_for('task'))

    return render_template('create_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET','POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.priority = request.form['priority']
        task.status = request.form['status']

        bd.session.commit()

        return redirect(url_for('task'))
    return render_template("edit_task.html", task=task)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    bd.session.delete(task)
    bd.session.commit()

    return redirect(url_for('task'))

if __name__ == '__main__':
    app.run(port=5001)
