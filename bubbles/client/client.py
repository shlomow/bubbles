import bubbles.readers
import requests
import bubbles.protocol


def upload_sample(host, port, path):
    '''Upload samples to the server

    :param host: hostname that the client connects to.
    :type host: str
    :param port: port number of the server.
    :type port: int
    :param path: path to where the snapshots are placed.
    :type path: str
    '''
    url = f'http://{host}:{port}/snapshot'
    reader = bubbles.readers.Reader(path, format='protobuf')
    for snapshot in reader:
        message = bubbles.protocol.serialize_message(reader.user, snapshot)
        requests.post(url,
                      data=message,
                      headers={'Content-Type': 'application/protobuf'})
