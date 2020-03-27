from bubbles.saver import Saver
import json
import subprocess


def test_pose(tmp_engine):
    url, engine = tmp_engine
    saver = Saver(url)
    data = {
        'user_id': 1,
        'translation': [2, 3, 4],
        'rotation': [5, 6, 7, 8]
    }

    expected = {
        'user_id': 1,
        'translation_x': 2,
        'translation_y': 3,
        'translation_z': 4,
        'rotation_x': 5,
        'rotation_y': 6,
        'rotation_z': 7,
        'rotation_w': 8,
    }
    json_data = json.dumps(data)
    saver.save('pose', json_data)

    query = 'SELECT * FROM pose'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == expected


def test_pose_cli(tmp_path, tmp_engine):
    url, engine = tmp_engine
    data = {
        'user_id': 1,
        'translation': [2, 3, 4],
        'rotation': [5, 6, 7, 8]
    }

    expected = {
        'user_id': 1,
        'translation_x': 2,
        'translation_y': 3,
        'translation_z': 4,
        'rotation_x': 5,
        'rotation_y': 6,
        'rotation_z': 7,
        'rotation_w': 8,
    }
    json_data = json.dumps(data)
    path = tmp_path / 'pose.result'
    path.write_text(json_data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.saver', 'save', '-d', url,
         'pose', str(path)]
    )

    process.communicate()

    query = 'SELECT * FROM pose'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == expected
