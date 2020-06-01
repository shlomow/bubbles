import flask
import json
import requests

glob_api_host = None
glob_api_port = None
gui_server = flask.Flask(__name__)


@gui_server.route('/')
def get_home():
    url = f'http://{glob_api_host}:{glob_api_port}/users'
    users = json.loads(requests.get(url).text)
    users_list = []
    for user in users:
        user_id = user['user_id']
        user = json.loads(requests.get(f'{url}/{user_id}').text)
        users_list.append(user)

    return flask.render_template('home.html', users=users_list)


@gui_server.route('/users/<user_id>/snapshots')
def get_snapshots(user_id):
    url = f'http://{glob_api_host}:{glob_api_port}/users/{user_id}/snapshots'
    snapshots = json.loads(requests.get(url).text)
    return flask.render_template('snapshots.html',
                                 snapshots=snapshots,
                                 user_id=user_id)


@gui_server.route('/users/<user_id>/snapshots/<snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    url = f'http://{glob_api_host}:{glob_api_port}'
    url = f'{url}/users/{user_id}/snapshots/<snapshot_id>'
    snapshots = json.loads(requests.get(url).text)
    return flask.render_template('snapshots.html',
                                 snapshots=snapshots,
                                 user_id=user_id)


def run_server(host, port, api_host, api_port):
    global glob_api_port, glob_api_host
    glob_api_host = api_host
    glob_api_port = api_port
    gui_server.run(host=host, port=port)
