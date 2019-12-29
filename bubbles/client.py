import bubbles.reader
import requests
from bubbles.protocol.serializer import Serializer


def upload_snapshots(address, path):
    url = f'http://{address[0]}:{address[1]}/snapshot'
    reader = bubbles.reader.Reader(path, 'protobuf')
    config = None
    serializer = Serializer('json', config)
    for snapshot in reader:
        requests.post(url, json=serializer.serialize(reader.user, snapshot))