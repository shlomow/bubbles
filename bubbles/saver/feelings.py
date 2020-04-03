import sqlalchemy as db


def save_feelings(engine, feelings):
    metadata = db.MetaData()
    table = db.Table('feelings', metadata,
                     db.Column('snapshot_id', db.Integer),
                     db.Column('hunger', db.Float),
                     db.Column('thirst', db.Float),
                     db.Column('exhaustion', db.Float),
                     db.Column('happiness', db.Float))

    metadata.create_all(engine)

    insert = table.insert().values(feelings)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_feelings.name = 'feelings'
