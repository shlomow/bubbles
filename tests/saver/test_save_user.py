from bubbles.saver import Saver
import json
import subprocess


def test_user(tmp_engine):
    url, engine = tmp_engine
    saver = Saver(url)
    data = {
        'user_id': 1,
        'username': 'dan',
        'gender': 0,
        'birthday': 12345678
    }
    json_data = json.dumps(data)
    saver.save('user', json_data)

    query = 'SELECT * FROM users'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data


def test_user_cli(tmp_path, tmp_engine):
    url, engine = tmp_engine
    data = {
        'user_id': 1,
        'username': 'dan',
        'gender': 0,
        'birthday': 12345678
    }
    json_data = json.dumps(data)
    path = tmp_path / 'user.result'
    path.write_text(json_data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.saver', 'save', '-d', url,
         'user', str(path)]
    )

    process.communicate()

    query = 'SELECT * FROM users'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data
