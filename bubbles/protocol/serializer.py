import struct
import bubbles.protobuf.bubbles_pb2 as bubbles_proto
from io import BytesIO


def deserialize_message(data):
    stream = BytesIO(data)
    user_size, = struct.unpack('<I', stream.read(4))
    user = bubbles_proto.User()
    user.ParseFromString(stream.read(user_size))

    snapshot_size, = struct.unpack('<I', stream.read(4))
    snapshot = bubbles_proto.Snapshot()
    snapshot.ParseFromString(stream.read(snapshot_size))

    return user, snapshot


def serialize_message(user, snapshot):
    user_data = user.SerializeToString()
    user_size = struct.pack('<I', len(user_data))

    snapshot_data = snapshot.SerializeToString()
    snapshot_size = struct.pack('<I', len(snapshot_data))
    return user_size + user_data + snapshot_size + snapshot_data
