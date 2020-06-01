import sqlalchemy as db


def save_user(engine, user):
    '''Save user to db.

    :param engine: sqlalchemy engine object.
    :param user: json which was returned by user parser.
    '''
    metadata = db.MetaData()
    table = db.Table('users', metadata,
                     db.Column('user_id', db.Integer, primary_key=True),
                     db.Column('username', db.String),
                     db.Column('gender', db.Integer),
                     db.Column('birthday', db.Integer))

    metadata.create_all(engine)

    user = {'user_id': user['user_id'],
            'username': user['username'],
            'gender': user['gender'],
            'birthday': user['birthday']}

    insert = table.insert().values(user)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_user.name = 'user'
