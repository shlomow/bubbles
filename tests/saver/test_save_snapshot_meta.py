from bubbles.saver import Saver
import json
import subprocess


def test_feelings(tmp_engine):
    url, engine = tmp_engine
    saver = Saver(url)
    data = {
        'snapshot_id': 1,
        'user_id': 5,
        'datetime': 'hello'
    }
    json_data = json.dumps(data)
    saver.save('snapshot_meta', json_data)

    query = 'SELECT * FROM snapshots'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data


def test_feelings_cli(tmp_path, tmp_engine):
    url, engine = tmp_engine
    data = {
        'snapshot_id': 1,
        'user_id': 5,
        'datetime': 'hello'
    }
    json_data = json.dumps(data)
    path = tmp_path / 'snapshot_meta.result'
    path.write_text(json_data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.saver', 'save', '-d', url,
         'snapshot_meta', str(path)]
    )

    process.communicate()

    query = 'SELECT * FROM snapshots'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data
