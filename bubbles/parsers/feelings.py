def parse_feelings(snapshot):
    return {'hunger': snapshot.Feelings.hunger,
            'thirst': snapshot.Feelings.thirst,
            'exhaustion': snapshot.Feelings.exhaustion,
            'happiness': snapshot.Feelings.happiness}


parse_feelings.name = 'feelings'
