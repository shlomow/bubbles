import sqlalchemy as db


def save_color_image(engine, color_image):
    metadata = db.MetaData()
    table = db.Table('color_image', metadata,
                     db.Column('user_id', db.Integer),
                     db.Column('path', db.String, nullable=False))

    metadata.create_all(engine)

    insert = table.insert().values(color_image)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_color_image.name = 'color_image'
