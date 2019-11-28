import pathlib
import struct
import datetime as dt
import threading
import contextlib
import bubbles.utils as utils


class ClientHandler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def receive_header(self):
        header_size = struct.calcsize('QQI')
        header = self.connection.receive(header_size)
        return struct.unpack('QQI', header)

    def receive_packet(self):
        (user_id, timestamp, thought_size) = self.receive_header()
        thought = self.connection.receive(thought_size)
        return (user_id, timestamp, thought_size, thought)

    def run(self):
        (user_id, timestamp, _, thought) = self.receive_packet()
        dt_timestamp = dt.datetime.fromtimestamp(timestamp)
        filename = dt_timestamp.strftime('%Y-%m-%d_%H-%M-%S.txt')
        self.lock.acquire()
        try:
            user_dir_path = pathlib.Path(self.data_dir) / str(user_id)
            if not user_dir_path.exists():
                user_dir_path.mkdir(parents=True, exist_ok=True)

            full_path = user_dir_path / filename
            if full_path.exists():
                payload = '\n' + thought.decode()
            else:
                payload = thought.decode()
            with full_path.open(mode='a') as fid:
                fid.write(payload)

        finally:
            self.lock.release()
            self.connection.close()


def run_server(address, data_dir):
    with contextlib.suppress(KeyboardInterrupt):
        server = utils.Listener(address[1], host=address[0])
        server.start()

        while True:
            client = server.accept()
            client_handler = ClientHandler(client, data_dir)
            client_handler.start()
