import datetime as dt


def parse_snapshot_meta(context, user, snapshot):
    timestamp = snapshot.datetime / 1000
    return {'snapshot_id': snapshot.datetime,
            'user_id': user.user_id,
            'datetime': str(dt.datetime.fromtimestamp(timestamp))}


parse_snapshot_meta.name = 'snapshot_meta'
