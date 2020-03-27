import flask


class Server:
    def __init__(self, host, port, publish):
        self.host = host
        self.port = port
        self.publish = publish
        self.app = flask.Flask(__name__)
        self.app.add_url_rule('/snapshot', 'snapshot', self.snapshot,
                              methods=['POST'])

    def snapshot(self):
        try:
            self.publish(flask.request.data)
            return ""
        except Exception as e:
            return flask.jsonify({'error': str(e)}), 500

    def run(self):
        self.app.run(host=self.host, port=self.port)


def run_server(host, port, publish):
    server = Server(host, port, publish)
    server.run()
