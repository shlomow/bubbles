from bubbles.readers.proto import ProtoReader
import bubbles.protobuf.bubbles_pb2 as bubbles_proto
import pytest
import datetime as dt
import struct
from io import BytesIO

# user parameters
_USER_ID = 5
_USERNAME = 'shlomi'
_BIRTHDAY = dt.datetime(1993, 9, 28)
_GENDER = 0

# snapshot parameters
_SNAPSHOT_DATETIME = dt.datetime(2007, 12, 28, 5, 45, 7)

_POSE = bubbles_proto.Pose()
_POSE.translation.x = 1
_POSE.translation.y = 2
_POSE.translation.z = 3
_POSE.rotation.x = 4
_POSE.rotation.y = 5
_POSE.rotation.z = 6
_POSE.rotation.w = 7

_FEELINGS = bubbles_proto.Feelings()
_FEELINGS.hunger = 1
_FEELINGS.thirst = 2
_FEELINGS.exhaustion = 3
_FEELINGS.happiness = 4

_COLOR_IMAGE = bubbles_proto.ColorImage()
_COLOR_IMAGE.width = 1
_COLOR_IMAGE.height = 2
_COLOR_IMAGE.data = bytes([1, 2, 3, 4, 5, 6])

_DEPTH_IMAGE = bubbles_proto.DepthImage()
_DEPTH_IMAGE.width = 1
_DEPTH_IMAGE.height = 2
_DEPTH_IMAGE.data.extend([1, 2])


@pytest.fixture
def user():
    user_proto = bubbles_proto.User()
    user_proto.user_id = _USER_ID
    user_proto.username = _USERNAME
    user_proto.birthday = int(_BIRTHDAY.timestamp())
    user_proto.gender = _GENDER

    return user_proto


@pytest.fixture
def snapshot():
    snapshot_proto = bubbles_proto.Snapshot()
    snapshot_proto.datetime = int(_SNAPSHOT_DATETIME.timestamp() * 1000)
    snapshot_proto.pose.CopyFrom(_POSE)
    snapshot_proto.feelings.CopyFrom(_FEELINGS)
    snapshot_proto.color_image.CopyFrom(_COLOR_IMAGE)
    snapshot_proto.depth_image.CopyFrom(_DEPTH_IMAGE)

    return snapshot_proto


def test_proto_reader(user, snapshot):
    user_data = user.SerializeToString()
    user_size = struct.pack('<I', len(user_data))

    snapshot_data = snapshot.SerializeToString()
    snapshot_size = struct.pack('<I', len(snapshot_data))

    stream = BytesIO(user_size + user_data + snapshot_size + snapshot_data)
    reader = ProtoReader(stream)

    assert reader.user == user

    snapshots_iter = iter(reader)
    assert next(snapshots_iter) == snapshot
    with pytest.raises(StopIteration):
        next(snapshots_iter)
