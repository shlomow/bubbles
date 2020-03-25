import struct


def deserialize_message(data):
    pass


def serialize_message(user, snapshot):
    user_data = user.SerializeToString()
    user_size = struct.pack('<I', len(user_data))

    snapshot_data = snapshot.SerializeToString()
    snapshot_size = struct.pack('<I', len(snapshot_data))
    return user_size + user_data + snapshot_size + snapshot_data
