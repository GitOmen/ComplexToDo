import json
from http import HTTPStatus

from flask import Flask, Response, request

import services

MIME = 'application/json'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


def build_response(body=None, status=HTTPStatus.OK):
    response = ''
    if body is not None:
        response = json.dumps(body)
    return Response(response, status=status, mimetype=MIME)


@app.route('/')
def hello_world():
    return build_response("It's LightToDoApp!")


@app.route("/tasks", methods=['POST'])
def add_task():
    request_data = request.get_json()
    try:
        return build_response(services.add_task(request_data))
    except services.InvalidStatusException as exc:
        return build_response({'error': str(exc)}, HTTPStatus.BAD_REQUEST)


@app.route('/tasks')
def get_all_tasks():

    return build_response(services.get_all_tasks())


@app.route('/tasks/<int:id>')
def get_task(id):
    try:
        return build_response(services.get_task(id))
    except services.TaskDoesNotExistException as exc:
        return build_response({'error': str(exc)}, HTTPStatus.NOT_FOUND)


@app.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    request_data = request.get_json()
    try:
        return build_response(services.update_task(id, request_data))
    except services.TaskDoesNotExistException as exc:
        return build_response({'error': str(exc)}, HTTPStatus.NOT_FOUND)
    except services.InvalidStatusException as exc:
        return build_response({'error': str(exc)}, HTTPStatus.BAD_REQUEST)


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        services.delete_task(id)
        return build_response(status=HTTPStatus.NO_CONTENT)
    except services.TaskDoesNotExistException as exc:
        return build_response({'error': str(exc)}, HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
