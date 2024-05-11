from Objects.Pose import Pose


def calculate_pose_timeseries(robot, act_states_time_series):
    pose_time_series = []

    for i in range(len(act_states_time_series)):
        act_states = act_states_time_series[i]
        robot.set_act_states_t_1(act_states)

        pose_time_series.append(Pose(robot))

    return pose_time_series

def calculate_pose_timeseries_origin(robot, act_states_time_series, org_time_series):
    pose_time_series = []

    for i in range(len(act_states_time_series)):
        act_states = act_states_time_series[i]
        robot.set_act_states_t_1(act_states)

        origin = org_time_series[i]
        robot.set_new_origin(origin)

        pose_time_series.append(Pose(robot))

    return pose_time_series
