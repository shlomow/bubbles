import datetime as dt
import json
from bubbles.utils import create_stream
from bubbles.parsers import run_parser
import subprocess
from bubbles.utils import Context


def test_depth_image(user, snapshot):
    data = create_stream(user, [snapshot]).read()
    result = run_parser('depth_image', data)
    timestamp = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    out_path = Context.work_path + f'/depth_image-{str(timestamp)}.jpg'
    expected = {
        'user_id': user.user_id,
        'path': out_path
    }
    assert json.loads(result) == expected


def test_depth_image_cli(tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.parsers', 'parse', 'depth_image', str(path)],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    timestamp = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    out_path = Context.work_path + f'/depth_image-{str(timestamp)}.jpg'
    expected = {
        'user_id': user.user_id,
        'path': out_path
    }

    assert json.loads(stdout) == expected
