from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    response = requests.get('http://localhost:5001/jobs')
    return jsonify(response.json())

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    response = requests.post('http://localhost:5001/jobs', json=data)
    return jsonify(response.json())

@app.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    response = requests.put(f'http://localhost:5001/jobs/{job_id}', json=data)
    return jsonify(response.json())

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    response = requests.delete(f'http://localhost:5001/jobs/{job_id}')
    return jsonify(response.json())

@app.route('/employees', methods=['GET'])
def get_employees():
    response = requests.get('http://localhost:5002/employees')
    return jsonify(response.json())

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    response = requests.post('http://localhost:5002/employees', json=data)
    return jsonify(response.json())

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    response = requests.put(f'http://localhost:5002/employees/{employee_id}', json=data)
    return jsonify(response.json())

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    response = requests.delete(f'http://localhost:5002/employees/{employee_id}')
    return jsonify(response.json())

@app.route('/projects', methods=['GET'])
def get_projects():
    response = requests.get('http://localhost:5003/projects')
    return jsonify(response.json())

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    response = requests.post('http://localhost:5003/projects', json=data)
    return jsonify(response.json())

@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    response = requests.put(f'http://localhost:5003/projects/{project_id}', json=data)
    return jsonify(response.json())

@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    response = requests.delete(f'http://localhost:5003/projects/{project_id}')
    return jsonify(response.json())

@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = requests.get('http://localhost:5004/tasks')
    return jsonify(response.json())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    response = requests.post('http://localhost:5004/tasks', json=data)
    return jsonify(response.json())

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    response = requests.put(f'http://localhost:5004/tasks/{task_id}', json=data)
    return jsonify(response.json())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    response = requests.delete(f'http://localhost:5004/tasks/{task_id}')
    return jsonify(response.json())

if __name__ == '__main__':
    app.run()
