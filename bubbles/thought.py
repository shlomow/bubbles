import struct
import datetime

class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, timestamp={self.timestamp!r}, thought="{self.thought}")'

    def __str__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'[{timestamp_str}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False

        return self.user_id == other.user_id and \
                self.timestamp == other.timestamp and \
                self.thought == other.thought

    def serialize(self):
        return struct.pack('QQI', self.user_id, int((self.timestamp - datetime.datetime(1970, 1, 1, 2)).total_seconds()), len(self.thought)) + bytes(self.thought, 'utf-8')

    def deserialize(packet):
        header_size = struct.calcsize('QQI')
        header = packet[:header_size]
        (user_id, timestamp, thought_size) = struct.unpack('QQI', header)
        return Thought(user_id, datetime.datetime.fromtimestamp(timestamp), packet[header_size:].decode('utf-8'))

