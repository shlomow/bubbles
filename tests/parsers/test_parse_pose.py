import json
from bubbles.utils import create_stream
from bubbles.parsers import run_parser
import subprocess


def test_pose(user, snapshot):
    data = create_stream(user, [snapshot]).read()
    result = run_parser('pose', data)
    expected = {
        'snapshot_id': snapshot.datetime,
        'translation': [snapshot.pose.translation.x,
                        snapshot.pose.translation.y,
                        snapshot.pose.translation.z],
        'rotation': [snapshot.pose.rotation.x,
                     snapshot.pose.rotation.y,
                     snapshot.pose.rotation.z,
                     snapshot.pose.rotation.w]
    }
    assert json.loads(result) == expected


def test_pose_cli(tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.parsers', 'parse', 'pose', str(path)],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    expected = {
        'snapshot_id': snapshot.datetime,
        'translation': [snapshot.pose.translation.x,
                        snapshot.pose.translation.y,
                        snapshot.pose.translation.z],
        'rotation': [snapshot.pose.rotation.x,
                     snapshot.pose.rotation.y,
                     snapshot.pose.rotation.z,
                     snapshot.pose.rotation.w]
    }

    assert json.loads(stdout) == expected
