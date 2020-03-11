import flask


class Server:
    def __init__(self, host, port, publish):
        self.host = host
        self.port = port
        self.publish = publish
        self.app = flask.Flask(__name__)
        self.load_modules()
        self.app.add_url_rule('/snapshot', 'snapshot', self.snapshot, methods=['POST'])

    def load_modules(self):
        self.modules = dict()
        
    def snapshot(self):
        self.publish(flask.request.data)
        return flask.jsonify({'return_value': 3, 'error': None})

    def run(self):
        self.app.run(host=self.host, port=self.port)


def run_server(host, port, publish):
    server = Server(host, port, publish)
    server.run()


if __name__ == '__main__':
    run_server(('localhost', 5000))
