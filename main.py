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


@app.route("/tasks/new", methods=['POST'])
def add_task():
    request_data = request.get_json()

    return build_response(services.add_to_list(request_data))


@app.route('/tasks/all')
def get_all_tasks():

    return build_response(services.get_all_tasks())


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):

    return build_response(services.get_task(id))


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    request_data = request.get_json()

    return build_response(services.update_task(id, request_data))
    #
    # if respond_data is None:
    #     response = response_error(f"{{'error': 'Error updating task - {task_name},  {status}'}}", 400)
    #     return response
    #
    # response = Response(json.dumps(respond_data), mimetype=MIME)
    # return response


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    services.delete_task(id)
    return build_response(status=HTTPStatus.NO_CONTENT)

    # if respond_data is None:
    #     response = response_error(f"{{'error': 'Error deleting task - {task_name}'}}", 400)
    #     return response
    #
    # response = Response(json.dumps(respond_data), mimetype=MIME)
    # return response


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
