from pytest_cov.embed import cleanup_on_sigterm
import pickle
import time
import bubbles.server
import pytest
import multiprocessing
import requests

cleanup_on_sigterm()  # see https://pytest-cov.readthedocs.io/en/v2.6.1/mp.html

_HOST = 'localhost'
_PORT = 8000


class MockPublish:
    def __init__(self, process):
        self.process = process
        self.args = None
        self.kwargs = None

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.process.send(pickle.dumps(self))

    def assert_called_with(self, *args, **kwargs):
        assert self.args == args
        assert self.kwargs == kwargs


@pytest.fixture
def server_pipe():
    parent, child = multiprocessing.Pipe()
    mock_publish = MockPublish(child)
    process = multiprocessing.Process(
                    target=_run_server,
                    args=(child, mock_publish))

    process.start()
    parent.recv()
    try:
        yield parent

    finally:
        process.terminate()
        process.join()


@pytest.mark.parametrize('msg', [(b'hello', 200)])
def test_server(server_pipe, msg):
    url = f'http://{_HOST}:{_PORT}/snapshot'
    time.sleep(0.2)
    msg_data, expected_response_code = msg
    res = requests.post(url, msg_data)
    assert res.status_code == expected_response_code
    mock_publish = server_pipe.recv()
    mock_publish = pickle.loads(mock_publish)
    mock_publish.assert_called_with(msg_data)


def _run_server(pipe, publish):
    pipe.send('read')
    bubbles.server.run_server(_HOST, _PORT, publish)
