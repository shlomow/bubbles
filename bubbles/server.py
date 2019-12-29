from flask import Flask


app = Flask(__name__)


@app.route('/snapshot', methods=['POST'])
def snapshot():
    print('snapshot received')
    return "ok"


def run_server(address):
    app.run(host=address[0], port=address[1])