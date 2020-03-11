import bubbles.readers
import requests
import bubbles.protocol


def upload_sample(host, port, path):
    url = f'http://{host}:{port}/snapshot'
    reader = bubbles.readers.Reader(path, format='protobuf')
    for snapshot in reader:
        message = bubbles.protocol.serialize_message(reader.user, snapshot)
        requests.post(url,
                      data=message,
                      headers={'Content-Type': 'application/protobuf'})
