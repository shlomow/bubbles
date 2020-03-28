def parse_user(context, user, snapshot):
    return {'user_id': user.user_id,
            'username': user.username,
            'gender': user.gender,
            'birthday': user.birthday}


parse_user.name = 'user'
