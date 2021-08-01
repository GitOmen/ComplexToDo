import json
from http import HTTPStatus

from flask import Flask, Response, request

import services

app = Flask(__name__)


def build_response(body=None, status=HTTPStatus.OK):
    response = ''
    if body is not None:
        response = json.dumps(body)
    return Response(response, status=status, mimetype='application/json')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
    return response


@app.errorhandler(services.TaskDoesNotExistException)
def handle_task_does_not_exist(exc):
    return build_response({'error': str(exc)}, HTTPStatus.NOT_FOUND)


@app.errorhandler(services.TaskListDoesNotExistException)
def handle_task_list_does_not_exist(exc):
    return build_response({'error': str(exc)}, HTTPStatus.NOT_FOUND)


@app.errorhandler(services.InvalidStatusException)
def handle_invalid_status(exc):
    return build_response({'error': str(exc)}, HTTPStatus.BAD_REQUEST)


@app.route('/')
def hello_world():
    return build_response("It's LightToDoApp!")


@app.route("/tasks", methods=['POST'])
def add_task():
    request_data = request.get_json()
    return build_response(services.add_task(request_data))


@app.route('/tasks')
def get_all_tasks():
    return build_response(services.get_all_tasks())


@app.route('/tasks/<int:id>')
def get_task(id):
    return build_response(services.get_task(id))


@app.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    request_data = request.get_json()
    return build_response(services.update_task(id, request_data))


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    services.delete_task(id)
    return build_response(status=HTTPStatus.NO_CONTENT)


@app.route("/lists", methods=['POST'])
def add_list():
    request_data = request.get_json()
    return build_response(services.add_task_list(request_data))


@app.route('/lists')
def get_all_lists():
    return build_response(services.get_all_task_lists())


@app.route('/lists/<int:id>')
def get_list(id):
    return build_response(services.get_task_list(id))


@app.route('/lists/<int:id>', methods=['PATCH'])
def update_task_list(id):
    request_data = request.get_json()
    return build_response(services.update_task_list(id, request_data))


@app.route('/lists/<int:id>', methods=['DELETE'])
def delete_task_list(id):
    services.delete_task_list(id)
    return build_response(status=HTTPStatus.NO_CONTENT)


@app.route('/lists/<int:id>/tasks')
def get_list_tasks(id):
    return build_response(services.get_all_tasks(id))


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
