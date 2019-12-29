import struct
from bubbles import user
from bubbles import snapshot


class BinaryReader:
    def __init__(self, stream):
        self.stream = stream
        user_id, = struct.unpack('<Q', self.stream.read(8))
        username_size, = struct.unpack('<I', self.stream.read(4))
        username = self.stream.read(username_size).decode()
        birthdate, = struct.unpack('<I', self.stream.read(4))
        gender = self.stream.read(1).decode()
        self.user = user.User(user_id, username, birthdate, gender)

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            timestamp, = struct.unpack('<Q', self.stream.read(8))
            timestamp /= 1000   # convert from milliseconds to seconds
            translation = struct.unpack('<3d', self.stream.read(struct.calcsize('<3d')))
            rotation = struct.unpack('<4d', self.stream.read(struct.calcsize('<4d')))
            color_image_height, color_image_width = struct.unpack('<II', self.stream.read(8))
            color_image = list()
            for _ in range(color_image_height * color_image_width):
                pixel_bgr = self.stream.read(3)
                r, g, b = pixel_bgr[2], pixel_bgr[1], pixel_bgr[0]
                color_image.append((r, g, b))
                
            depth_image_height, depth_image_width = struct.unpack('<II', self.stream.read(8))
            depth_image_size = depth_image_height * depth_image_width
            depth_image = struct.unpack(f'<{depth_image_size}f', self.stream.read(4 * depth_image_height * depth_image_width))
            feelings = struct.unpack('<4f', self.stream.read(struct.calcsize('<4f')))

            return snapshot.Snapshot(timestamp, translation, rotation,
                color_image, (color_image_width, color_image_height),
                depth_image, (depth_image_width, depth_image_height), feelings)
        
        except Exception:
            raise StopIteration