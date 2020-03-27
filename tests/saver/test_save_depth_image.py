from bubbles.saver import Saver
import json
import subprocess


def test_depth_image(tmp_engine):
    url, engine = tmp_engine
    saver = Saver(url)
    data = {'user_id': 1, 'path': '/hello/world'}
    json_data = json.dumps(data)
    saver.save('depth_image', json_data)

    query = 'SELECT * FROM depth_image'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data


def test_depth_image_cli(tmp_path, tmp_engine):
    url, engine = tmp_engine
    data = {'user_id': 1, 'path': '/hello/world'}
    json_data = json.dumps(data)
    path = tmp_path / 'depth_image.result'
    path.write_text(json_data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.saver', 'save', '-d', url,
         'depth_image', str(path)]
    )

    process.communicate()

    query = 'SELECT * FROM depth_image'

    with engine.connect() as conn:
        for row in conn.execute(query):
            assert dict(row) == data
