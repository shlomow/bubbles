from sqlalchemy import create_engine
import flask
import json


api_db_engine = None
api_server = flask.Flask(__name__)


@api_server.route('/users')
def get_users():
    query = 'SELECT user_id, username FROM users'
    out_list = []
    with api_db_engine.connect() as conn:
        for row in conn.execute(query):
            out_list.append(dict(row))

    return json.dumps(out_list)


@api_server.route('/users/<user_id>')
def get_user(user_id):
    query = f'SELECT * FROM users WHERE user_id={user_id}'
    out_list = []
    with api_db_engine.connect() as conn:
        for row in conn.execute(query):
            out_list.append(dict(row))

    if out_list:
        return json.dumps(out_list[0])  # should be only one result
    return "", 404


@api_server.route('/users/<user_id>/snapshots')
def get_snapshots(user_id):
    query = f'SELECT snapshot_id, datetime FROM snapshots '\
            f'WHERE user_id={user_id}'
    out_list = []
    with api_db_engine.connect() as conn:
        for row in conn.execute(query):
            out_list.append(dict(row))

    return json.dumps(out_list)


@api_server.route('/users/<user_id>/snapshots/<snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    query = f'SELECT snapshot_id, datetime FROM snapshots '\
            f'WHERE user_id={user_id}'
    snapshot_details = []
    with api_db_engine.connect() as conn:
        for row in conn.execute(query):
            snapshot_details.append(dict(row))

    topics = ['pose', 'feelings', 'color_image', 'depth_image']
    if not snapshot_details:
        return "", 404

    out = snapshot_details[0]
    out['available_topics'] = []
    for topic in topics:
        query = f'SELECT count(*) FROM {topic} WHERE snapshot_id={snapshot_id}'
        with api_db_engine.connect() as conn:
            for row in conn.execute(query):
                out['available_topics'].append(topic)
                break

    if out:
        return json.dumps(out)  # should be only one result
    return "", 404


def run_api_server(host, port, database_url):
    global api_db_engine
    api_db_engine = create_engine(database_url)
    api_server.run(host=host, port=port)
