import datetime as dt


def parse_snapshot_meta(context, user, snapshot):
    '''Parse snapshot metadata from a given snapshot.

    :param context: context given from the application.
    :param user: user object parsed from the protocol
        between client and server.
    :param snapshot: snapshot object parsed from the protocol
        between client and server.
    :return: dictionary with `snapshot_id`, `user_id` and `datetime`.
    :rtype: dict
    '''
    timestamp = snapshot.datetime / 1000
    return {'snapshot_id': snapshot.datetime,
            'user_id': user.user_id,
            'datetime': str(dt.datetime.fromtimestamp(timestamp))}


parse_snapshot_meta.name = 'snapshot_meta'
