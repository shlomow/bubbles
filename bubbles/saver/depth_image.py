import sqlalchemy as db


def save_depth_image(engine, depth_image):
    '''Save depth image to db.

    :param engine: sqlalchemy engine object.
    :param depth_image: json which was returned by depth image parser.
    '''
    metadata = db.MetaData()
    table = db.Table('depth_image', metadata,
                     db.Column('snapshot_id', db.BigInteger),
                     db.Column('path', db.String, nullable=False))

    metadata.create_all(engine)

    insert = table.insert().values(depth_image)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_depth_image.name = 'depth_image'
