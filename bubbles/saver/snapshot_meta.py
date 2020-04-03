import sqlalchemy as db


def save_snapshot_meta(engine, snapshot_meta):
    metadata = db.MetaData()
    table = db.Table('snapshots', metadata,
                     db.Column('snapshot_id', db.Integer),
                     db.Column('user_id', db.Integer),
                     db.Column('datetime', db.String))

    metadata.create_all(engine)

    insert = table.insert().values(snapshot_meta)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_snapshot_meta.name = 'snapshot_meta'
