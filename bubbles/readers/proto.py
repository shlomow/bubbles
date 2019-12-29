import struct
from bubbles import user
from bubbles import snapshot
import bubbles.protobuf.bubbles_pb2 as bubbles_proto


class ProtoReader:
    def __init__(self, stream):
        self.stream = stream
        user_size, = struct.unpack('<I', self.stream.read(4))
        user_proto = bubbles_proto.User()
        user_proto.ParseFromString(self.stream.read(user_size))
        gender = bubbles_proto.User.Gender.Name(user_proto.gender)[0].lower()
        self.user = user.User(user_proto.user_id, user_proto.username,
            user_proto.birthday, gender)

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            snapshot_size, = struct.unpack('<I', self.stream.read(4))
            snapshot_proto = bubbles_proto.Snapshot()
            snapshot_proto.ParseFromString(self.stream.read(snapshot_size))

            timestamp = snapshot_proto.datetime / 1000
            translation = (snapshot_proto.pose.translation.x,
                snapshot_proto.pose.translation.y,
                snapshot_proto.pose.translation.z)
            rotation = (snapshot_proto.pose.rotation.x,
                snapshot_proto.pose.rotation.y,
                snapshot_proto.pose.rotation.z,
                snapshot_proto.pose.rotation.w)

            color_image = snapshot_proto.color_image.data
            color_image_width = snapshot_proto.color_image.width
            color_image_height = snapshot_proto.color_image.height

            depth_image = list(snapshot_proto.depth_image.data)
            depth_image_width = snapshot_proto.depth_image.width
            depth_image_height = snapshot_proto.depth_image.height

            feelings = (snapshot_proto.feelings.hunger,
                snapshot_proto.feelings.thirst,
                snapshot_proto.feelings.exhaustion,
                snapshot_proto.feelings.happiness)

            return snapshot.Snapshot(timestamp, translation, rotation,
                color_image, (color_image_width, color_image_height),
                depth_image, (depth_image_width, depth_image_height), feelings)
        
        except Exception:
            raise StopIteration