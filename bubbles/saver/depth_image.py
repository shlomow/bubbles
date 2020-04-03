import sqlalchemy as db


def save_depth_image(engine, depth_image):
    metadata = db.MetaData()
    table = db.Table('depth_image', metadata,
                     db.Column('snapshot_id', db.Integer),
                     db.Column('path', db.String, nullable=False))

    metadata.create_all(engine)

    insert = table.insert().values(depth_image)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_depth_image.name = 'depth_image'
