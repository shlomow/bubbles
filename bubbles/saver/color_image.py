import sqlalchemy as db


def save_color_image(engine, color_image):
    '''Save color image to db.

    :param engine: sqlalchemy engine object.
    :param color_image: json which was returned by color image parser.
    '''
    metadata = db.MetaData()
    table = db.Table('color_image', metadata,
                     db.Column('snapshot_id', db.BigInteger, primary_key=True),
                     db.Column('path', db.String, nullable=False))

    metadata.create_all(engine)

    insert = table.insert().values(color_image)
    with engine.connect() as connection:
        connection.execute(insert)


save_color_image.name = 'color_image'
