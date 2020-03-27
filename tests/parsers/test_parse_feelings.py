import json
from bubbles.utils import create_stream
from bubbles.parsers import run_parser
import subprocess


def test_feelings(user, snapshot):
    data = create_stream(user, [snapshot]).read()
    result = run_parser('feelings', data)
    expected = {
        'user_id': user.user_id,
        'hunger': snapshot.feelings.hunger,
        'thirst': snapshot.feelings.thirst,
        'exhaustion': snapshot.feelings.exhaustion,
        'happiness': snapshot.feelings.happiness
    }
    assert json.loads(result) == expected


def test_feelings_cli(tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.parsers', 'parse', 'feelings', str(path)],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    expected = {
        'user_id': user.user_id,
        'hunger': snapshot.feelings.hunger,
        'thirst': snapshot.feelings.thirst,
        'exhaustion': snapshot.feelings.exhaustion,
        'happiness': snapshot.feelings.happiness
    }

    assert json.loads(stdout) == expected
