import base64
import json
import datetime as dt


class Image:
    def __init__(self, data, resolution):
        self.data = data
        self.width = resolution[0]
        self.height = resolution[1]


class Snapshot:
    def __init__(self, timestamp, translation, rotation, color_image,
                 color_image_resolution, depth_image, depth_image_resolution,
                 feelings):
        self.timestamp = dt.datetime.fromtimestamp(timestamp)
        self.translation = translation
        self.rotation = rotation
        self.color_image = Image(color_image, color_image_resolution)
        self.depth_image = Image(depth_image, depth_image_resolution)
        self.feelings = feelings

    def __repr__(self):
        date_repr = self.timestamp.strftime('%B %d, %Y')
        time_repr = str(self.timestamp.time())
        return f'Snapshot from {date_repr} at {time_repr} on {self.translation}'\
               f' / {self.rotation} with a {self.color_image.width}x'\
               f'{self.color_image.height} color image and a '\
               f'{self.depth_image.width}x{self.depth_image.height}'\
               f' depth image'

    def dict(self):
        return dict(timestamp=int(self.timestamp.timestamp()),
                    translation=self.translation,
                    rotation=self.rotation,
                    color_image=base64.encodebytes(self.color_image.data).decode(),
                    depth_image=self.depth_image.data,
                    feelings=self.feelings)

    def json(self):
        return json.dumps(self.dict())