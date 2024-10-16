from enum import Enum


class RobotTask(Enum):
    initialize_connection = 'initialize_connection'
    reset_robot = 'reset_robot'
    set_actuator_states = 'set_actuator_states'
    set_end_effector = 'set_end_effector'
    set_origin = 'set_origin'
    get_pose = 'get_pose'
    stream_poses = 'stream_poses'
    stream_poses_for_new_origin = 'stream_poses_for_new_origin'
    stream_poses_for_new_origin_and_control_end_effector = 'stream_poses_for_new_origin_and_control_end_effector'
