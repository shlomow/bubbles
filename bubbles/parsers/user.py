def parse_user(context, user, snapshot):
    '''Parse user information from a given snapshot.

    :param context: context given from the application.
    :param user: user object parsed from the protocol
        between client and server.
    :param snapshot: snapshot object parsed from the protocol
        between client and server.
    :return: dictionary with user info.
    :rtype: dict
    '''
    return {'user_id': user.user_id,
            'username': user.username,
            'gender': user.gender,
            'birthday': user.birthday}


parse_user.name = 'user'
