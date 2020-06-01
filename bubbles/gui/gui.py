import flask
import json
import requests
import socket

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
    url = f'{url}/users/{user_id}/snapshots/{snapshot_id}'
    snapshot = json.loads(requests.get(url).text)
    for topic in snapshot['available_topics']:
        snapshot[topic] = json.loads(requests.get(f'{url}/{topic}').text)
    if 'color_image' in snapshot['available_topics']:
        snapshot['color_image'] = f'{url}/color_image/data'
    if 'depth_image' in snapshot['available_topics']:
        snapshot['depth_image'] = f'{url}/depth_image/data'
    return flask.render_template('snapshot.html',
                                 snapshot=snapshot)


def run_server(host, port, api_host, api_port):
    global glob_api_port, glob_api_host
    glob_api_host = socket.gethostbyname(api_host)
    glob_api_port = api_port
    gui_server.run(host=host, port=port)
