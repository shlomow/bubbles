import json
from bubbles.utils import create_stream
from bubbles.parsers import run_parser
import subprocess
import datetime as dt


def test_feelings(user, snapshot):
    data = create_stream(user, [snapshot]).read()
    result = run_parser('snapshot_meta', data)
    timestamp = snapshot.datetime / 1000
    expected = {
        'snapshot_id': snapshot.datetime,
        'user_id': user.user_id,
        'datetime': str(dt.datetime.fromtimestamp(timestamp))
    }
    assert json.loads(result) == expected


def test_feelings_cli(tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.parsers',
         'parse', 'snapshot_meta', str(path)],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    timestamp = snapshot.datetime / 1000
    expected = {
        'snapshot_id': snapshot.datetime,
        'user_id': user.user_id,
        'datetime': str(dt.datetime.fromtimestamp(timestamp))
    }

    assert json.loads(stdout) == expected
