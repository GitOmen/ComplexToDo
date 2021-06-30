import json

from flask import Flask, Response, request

import services

MIME = 'application/json'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


def response_error(error_msg, error_code):
    response = Response(error_msg, status=error_code, mimetype=MIME)
    return response


@app.route('/')
def hello_world():
    return "It's LightToDoApp!"


@app.route("/task/new", methods=['POST'])
def add_task():
    request_data = request.get_json()
    # task = request_data['task']

    services.add_to_list(request_data)
    return '', 204
    # respond_data = services.add_to_list(task)
    #
    # if respond_data is None:
    #     response = response_error(f"{{'error': 'Task not added - {task}'}}", 400)
    #     return response
    #
    # response = Response(json.dumps(respond_data), mimetype=MIME)
    # return response


@app.route('/tasks/all')
def get_all_tasks():

    response = Response(json.dumps(services.get_all_tasks()), mimetype=MIME)
    return response


@app.route('/task/status', methods=['GET'])
def get_task_status():
    task_name = request.args.get('name')
    status = services.get_task_status(task_name)

    if status is None:
        response = response_error(f"{{'error': 'Task Not Found - {task_name}'}}", 404)
        return response

    respond_data = {
        'status': status
    }
    response = Response(json.dumps(respond_data), status=200, mimetype=MIME)
    return response


@app.route('/task/update', methods=['PUT'])
def update_status():
    request_data = request.get_json()
    task_name = request_data['name']
    status = request_data['status']

    respond_data = services.update_status(task_name, status)

    if respond_data is None:
        response = response_error(f"{{'error': 'Error updating task - {task_name},  {status}'}}", 400)
        return response

    response = Response(json.dumps(respond_data), mimetype=MIME)
    return response


@app.route('/task/remove', methods=['DELETE'])
def delete_task():
    request_data = request.get_json()
    task_name = request_data['name']

    respond_data = services.delete_task(task_name)

    if respond_data is None:
        response = response_error(f"{{'error': 'Error deleting task - {task_name}'}}", 400)
        return response

    response = Response(json.dumps(respond_data), mimetype=MIME)
    return response


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
