import flask
import logging


app = flask.Flask(__name__)


@app.route('/snapshot', methods=['POST'])
def snapshot():
    data = flask.request.data
    return flask.jsonify({'return_value': 3, 'error': None})


def run_server(address):
    app.run(host=address[0], port=address[1])

if __name__ == '__main__':
    run_server(('localhost', 5000))
