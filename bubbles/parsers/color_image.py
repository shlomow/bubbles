from PIL import Image as PIL
import datetime as dt


def parse_color_image(context, user, snapshot):
    timestamp = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    path = context.path(f'color_image-{str(timestamp)}.jpg')
    size = snapshot.color_image.width, snapshot.color_image.height
    image = PIL.new('RGB', size)
    raw_data = snapshot.color_image.data
    pixels = [tuple(raw_data[i:i+3]) for i in range(0, len(raw_data), 3)]
    image.putdata(pixels)
    image.save(path)
    return {'user_id': user.user_id,
            'path': str(path)}


parse_color_image.name = 'color_image'
