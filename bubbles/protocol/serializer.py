import bubbles.protobuf.bubbles_pb2 as bubbles_proto


def serialize_message(user, snapshot):
    out_user = bubbles_proto.User()
    out_user.user_id = user.user_id
    out_user.username = user.username
    out_user.birthday = int(user.birthdate.timestamp())
    out_user.gender = bubbles_proto.User.Gender.Value(user.gender.upper())

    return out_user.SerializeToString()
