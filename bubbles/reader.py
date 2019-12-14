import struct
import datetime as dt


def is_all_file_read(fd):
    pass


class Snapshot:
    def __init__(self, timestamp, translation, rotation, color_image, depth_image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings


class Reader:
    def __init__(self, path):
        self.path = path
        self.fd = open(path, 'rb')
        self.user_id = struct.unpack('<Q', self.fd.read(8))
        username_size, = struct.unpack('<I', self.fd.read(4))
        self.username = self.fd.read(username_size).decode()
        self.timestamp = dt.datetime.fromtimestamp(int(struct.unpack('<I', self.fd.read(4))[0]))
        self.gender = self.fd.read(1).decode()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            timestamp, = struct.unpack('<Q', self.fd.read(8))
            timestamp /= 1000   # convert from milliseconds to seconds
            translation = struct.unpack('<3d', self.fd.read(struct.calcsize('<3d')))
            rotation = struct.unpack('<4d', self.fd.read(struct.calcsize('<4d')))
            color_image_height, color_image_width = struct.unpack('<II', self.fd.read(8))
            color_image = list()
            for _ in range(color_image_height * color_image_width):
                pixel_bgr = self.fd.read(3)
                r, g, b = pixel_bgr[2], pixel_bgr[1], pixel_bgr[0]
                color_image.append((r, g, b))
                
            depth_image_height, depth_image_width = struct.unpack('<II', self.fd.read(8))
            depth_image_size = depth_image_height * depth_image_width
            depth_image = struct.unpack(f'<{depth_image_size}f', self.fd.read(4 * depth_image_height * depth_image_width))
            feelings = struct.unpack('<4f', self.fd.read(struct.calcsize('<4f')))
            return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)
        except Exception:
            self.fd.close()
            raise StopIteration