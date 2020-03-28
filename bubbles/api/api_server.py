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


def run_api_server(host, port, database_url):
    global api_db_engine
    api_db_engine = create_engine(database_url)
    api_server.run(host=host, port=port)
