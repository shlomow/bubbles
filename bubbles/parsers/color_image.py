from PIL import Image as PIL
import datetime as dt


def parse_color_image(context, user, snapshot):
    '''Save color image as jpg to a file from a given snapshot.

    :param context: context given from the application,
        used to get a path to valid directory to save the image in.
    :param user: user object parsed from the protocol
        between client and server.
    :param snapshot: snapshot object parsed from the protocol
        between client and server.
    :return: dictionary with `snapshot_id` and `path` of the saved image.
    :rtype: dict
    '''
    timestamp = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    path = context.path(f'color_image-{str(timestamp)}.jpg')
    size = snapshot.color_image.width, snapshot.color_image.height
    image = PIL.new('RGB', size)
    raw_data = snapshot.color_image.data
    pixels = [tuple(raw_data[i:i+3]) for i in range(0, len(raw_data), 3)]
    image.putdata(pixels)
    image.save(path)
    return {'snapshot_id': snapshot.datetime,
            'path': str(path)}


parse_color_image.name = 'color_image'
