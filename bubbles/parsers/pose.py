def parse_pose(context, snapshot):
    context.print(snapshot.pose.rotation, snapshot.pose.translation)

parse_pose.field = 'pose'