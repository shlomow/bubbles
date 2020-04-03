def parse_feelings(context, user, snapshot):
    return {'snapshot_id': snapshot.datetime,
            'hunger': snapshot.feelings.hunger,
            'thirst': snapshot.feelings.thirst,
            'exhaustion': snapshot.feelings.exhaustion,
            'happiness': snapshot.feelings.happiness}


parse_feelings.name = 'feelings'
