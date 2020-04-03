from bubbles.saver import Saver
import json
import subprocess


def test_color_image(tmp_engine):
    url, engine = tmp_engine
    saver = Saver(url)
    data = {'snapshot_id': 1, 'path': '/hello/world'}
    json_data = json.dumps(data)
    saver.save('color_image', json_data)

    query = 'SELECT * FROM color_image'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data


def test_color_image_cli(tmp_path, tmp_engine):
    url, engine = tmp_engine
    data = {'snapshot_id': 1, 'path': '/hello/world'}
    json_data = json.dumps(data)
    path = tmp_path / 'color_image.result'
    path.write_text(json_data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.saver', 'save', '-d', url,
         'color_image', str(path)]
    )

    process.communicate()

    query = 'SELECT * FROM color_image'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data
