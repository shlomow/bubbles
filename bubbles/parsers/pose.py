def parse_pose(context, user, snapshot):
    '''Parse pose from a given snapshot.

    :param context: context given from the application.
    :param user: user object parsed from the protocol
        between client and server.
    :param snapshot: snapshot object parsed from the protocol
        between client and server.
    :return: dictionary with `snapshot_id`, rotation and translation of user.
    :rtype: dict
    '''
    return {'snapshot_id': snapshot.datetime,
            'rotation': [snapshot.pose.rotation.x,
                         snapshot.pose.rotation.y,
                         snapshot.pose.rotation.z,
                         snapshot.pose.rotation.w],
            'translation': [snapshot.pose.translation.x,
                            snapshot.pose.translation.y,
                            snapshot.pose.translation.z]}


parse_pose.name = 'pose'
