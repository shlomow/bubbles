import struct
import datetime as dt


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, ' \
               f'timestamp={self.timestamp!r}, thought="{self.thought}")'

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
        timestamp = int(self.timestamp.timestamp())
        return struct.pack('QQI', self.user_id, timestamp, len(self.thought)) \
            + bytes(self.thought, 'utf-8')

    def deserialize(packet):
        header_size = struct.calcsize('QQI')
        header = packet[:header_size]
        (user_id, timestamp, thought_size) = struct.unpack('QQI', header)
        thought = packet[header_size:].decode('utf-8')
        return Thought(user_id, dt.datetime.fromtimestamp(timestamp), thought)
