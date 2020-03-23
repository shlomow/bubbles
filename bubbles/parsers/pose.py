def parse_pose(context, user, snapshot):
    return {'id': user.user_id,
            'rotation': [snapshot.pose.rotation.x,
                         snapshot.pose.rotation.y,
                         snapshot.pose.rotation.z,
                         snapshot.pose.rotation.w],
            'translation': [snapshot.pose.translation.x,
                            snapshot.pose.translation.y,
                            snapshot.pose.translation.z]}


parse_pose.name = 'pose'
