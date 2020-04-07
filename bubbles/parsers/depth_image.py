import matplotlib.pyplot as plt
import datetime as dt


def parse_depth_image(context, user, snapshot):
    '''Save depth image as jpg to a file from a given snapshot.

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
    path = context.path(f'depth_image-{str(timestamp)}.jpg')
    width = snapshot.depth_image.width
    raw_data = snapshot.depth_image.data
    pixels = [raw_data[i:i+width] for i in range(0, len(raw_data), width)]
    plt.imshow(pixels, cmap='hot', interpolation='nearest')
    plt.savefig(path)
    return {'snapshot_id': snapshot.datetime,
            'path': str(path)}


parse_depth_image.name = 'depth_image'
