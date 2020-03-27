from bubbles.saver import Saver
import json
import subprocess


def test_feelings(tmp_engine):
    url, engine = tmp_engine
    saver = Saver(url)
    data = {
        'user_id': 1,
        'hunger': 5,
        'thirst': 6,
        'exhaustion': 7,
        'happiness': 8
    }
    json_data = json.dumps(data)
    saver.save('feelings', json_data)

    query = 'SELECT * FROM feelings'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data


def test_feelings_cli(tmp_path, tmp_engine):
    url, engine = tmp_engine
    data = {
        'user_id': 1,
        'hunger': 5,
        'thirst': 6,
        'exhaustion': 7,
        'happiness': 8
    }
    json_data = json.dumps(data)
    path = tmp_path / 'feelings.result'
    path.write_text(json_data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.saver', 'save', '-d', url,
         'feelings', str(path)]
    )

    process.communicate()

    query = 'SELECT * FROM feelings'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data
