import socket
import struct


class Connection:

    def __init__(self, sock):
        self.sock = sock

    def __repr__(self):
        sock_addr, sock_port = self.sock.getsockname()
        peer_addr, peer_port = self.sock.getpeername()

        return f'<Connection from {sock_addr}:{sock_port} to ' \
               f'{peer_addr}:{peer_port}>'

    def send(self, data):
        self.sock.sendall(data)

    def send_message(self, message):
        if isinstance(message, str):
            message = message.encode()
        message_size = struct.pack('<I', len(message))
        self.send(message_size + message)

    def receive(self, size):
        out = b''
        while size > 0:
            temp = self.sock.recv(size)
            if not temp:
                raise RuntimeError('socket closed')
            out += temp
            size -= len(temp)

        return out

    def receive_message(self):
        message_size = self.receive(struct.calcsize('<I'))
        message_size, = struct.unpack('<I', message_size)
        message = self.receive(message_size)
        return message

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)
