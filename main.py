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


@app.route("/task/new", methods=['POST'])
def add_task():
    request_data = request.get_json()

    services.add_to_list(request_data)
    return build_response(status=HTTPStatus.NO_CONTENT)


@app.route('/tasks/all')
def get_all_tasks():

    return build_response(services.get_all_tasks())


@app.route('/task/status', methods=['GET'])
def get_task_status():

    return build_response(services.get_task_status(request.args.get('name')))


@app.route('/task/update', methods=['PUT'])
def update_status():
    request_data = request.get_json()
    task_name = request_data['name']
    status = request_data['status']

    return build_response(services.update_status(task_name, status))
    #
    # if respond_data is None:
    #     response = response_error(f"{{'error': 'Error updating task - {task_name},  {status}'}}", 400)
    #     return response
    #
    # response = Response(json.dumps(respond_data), mimetype=MIME)
    # return response


@app.route('/task/remove', methods=['DELETE'])
def delete_task():
    request_data = request.get_json()
    task_name = request_data['name']

    return build_response(services.delete_task(task_name))

    # if respond_data is None:
    #     response = response_error(f"{{'error': 'Error deleting task - {task_name}'}}", 400)
    #     return response
    #
    # response = Response(json.dumps(respond_data), mimetype=MIME)
    # return response


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
