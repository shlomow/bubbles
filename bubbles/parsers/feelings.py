def parse_feelings(context, user, snapshot):
    return {'user_id': user.user_id,
            'hunger': snapshot.feelings.hunger,
            'thirst': snapshot.feelings.thirst,
            'exhaustion': snapshot.feelings.exhaustion,
            'happiness': snapshot.feelings.happiness}


parse_feelings.name = 'feelings'
