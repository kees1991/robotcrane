from enum import Enum


class RobotTask(Enum):
    initialize_robot = 'initialize_robot'
    reset_robot = 'reset_robot'
    get_pose = 'get_pose'
    move_actuators = 'move_actuators'
    move_end_effector = 'move_end_effector'
    move_origin = 'move_origin'
    move_origin_control_end_effector = 'move_origin_control_end_effector'
