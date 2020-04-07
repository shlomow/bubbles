import sqlalchemy as db


def save_snapshot_meta(engine, snapshot_meta):
    '''Save snapshot metadata to db.

    :param engine: sqlalchemy engine object.
    :param snapshot_meta: json which was returned by snapshot meta parser.
    '''
    metadata = db.MetaData()
    table = db.Table('snapshots', metadata,
                     db.Column('snapshot_id', db.BigInteger),
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
