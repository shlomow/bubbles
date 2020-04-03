import sqlalchemy as db


def save_pose(engine, pose):
    metadata = db.MetaData()
    table = db.Table('pose', metadata,
                     db.Column('snapshot_id', db.Integer),
                     db.Column('rotation_x', db.Float),
                     db.Column('rotation_y', db.Float),
                     db.Column('rotation_z', db.Float),
                     db.Column('rotation_w', db.Float),
                     db.Column('translation_x', db.Float),
                     db.Column('translation_y', db.Float),
                     db.Column('translation_z', db.Float))

    metadata.create_all(engine)

    pose = {'snapshot_id': pose['snapshot_id'],
            'rotation_x': pose['rotation'][0],
            'rotation_y': pose['rotation'][1],
            'rotation_z': pose['rotation'][2],
            'rotation_w': pose['rotation'][3],
            'translation_x': pose['translation'][0],
            'translation_y': pose['translation'][1],
            'translation_z': pose['translation'][2]}

    insert = table.insert().values(pose)
    connection = engine.connect()
    try:
        connection.execute(insert)
    finally:
        connection.close()


save_pose.name = 'pose'
