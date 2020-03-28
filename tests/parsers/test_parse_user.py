import json
from bubbles.utils import create_stream
from bubbles.parsers import run_parser
import subprocess


def test_user(user, snapshot):
    data = create_stream(user, [snapshot]).read()
    result = run_parser('user', data)
    expected = {
        'user_id': user.user_id,
        'username': user.username,
        'gender': user.gender,
        'birthday': user.birthday
    }

    assert json.loads(result) == expected


def test_user_cli(tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.parsers', 'parse', 'user', str(path)],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    expected = {
        'user_id': user.user_id,
        'username': user.username,
        'gender': user.gender,
        'birthday': user.birthday
    }

    assert json.loads(stdout) == expected
