import struct
import bubbles.protobuf.bubbles_pb2 as bubbles_proto


class ProtoReader:
    '''protobuf format snapshots reader implementation.
    '''
    format = 'protobuf'

    def __init__(self, stream):
        '''
        :param stream: stream of bytes that `ProtoReader` operates on.
        '''
        self.stream = stream
        user_size, = struct.unpack('<I', self.stream.read(4))
        user_proto = bubbles_proto.User()
        user_proto.ParseFromString(self.stream.read(user_size))
        self.user = user_proto

    def __iter__(self):
        return self

    def __next__(self):
        try:
            snapshot_size, = struct.unpack('<I', self.stream.read(4))
            snapshot_proto = bubbles_proto.Snapshot()
            snapshot_proto.ParseFromString(self.stream.read(snapshot_size))
            return snapshot_proto

        except Exception:
            raise StopIteration
