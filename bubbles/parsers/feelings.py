def parse_feelings(context, user, snapshot):
    '''Parse feelings from a given snapshot.

    :param context: context given from the application.
    :param user: user object parsed from the protocol
        between client and server.
    :param snapshot: snapshot object parsed from the protocol
        between client and server.
    :return: dictionary with `snapshot_id` and feelings of user.
    :rtype: dict
    '''
    return {'snapshot_id': snapshot.datetime,
            'hunger': snapshot.feelings.hunger,
            'thirst': snapshot.feelings.thirst,
            'exhaustion': snapshot.feelings.exhaustion,
            'happiness': snapshot.feelings.happiness}


parse_feelings.name = 'feelings'
