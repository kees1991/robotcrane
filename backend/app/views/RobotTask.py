from enum import Enum


class RobotTask(Enum):
    reset_robot = 'reset_robot'
    move_actuators = 'move_actuators'
    move_end_effector = 'move_end_effector'
    move_origin = 'move_origin'
    get_pose = 'get_pose'
    move_origin_control_end_effector = 'move_origin_control_end_effector'
