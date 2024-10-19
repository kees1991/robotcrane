import json

import numpy as np

from backend.app.models.ActuatorStates import ActuatorStates


def convert_to_xyz_tuple(frame: np.ndarray) -> tuple:
    frame_t = frame[0:3, 3:4].T
    return tuple(map(tuple, frame_t))[0]


class Pose(object):
    """
    Defining the robot pose including the origin for rendering it on the frontend
    The pose is represented by the xyz coordinates of all the joints and the rotation angles
    """

    def __init__(self, robot_frames: np.ndarray, origin_t_1: tuple, act_states_t_1: ActuatorStates):
        self.j_1 = convert_to_xyz_tuple(robot_frames[0])
        self.j_2 = convert_to_xyz_tuple(robot_frames[1])
        self.j_3 = convert_to_xyz_tuple(robot_frames[2])
        self.j_4 = convert_to_xyz_tuple(robot_frames[3])
        self.j_5 = convert_to_xyz_tuple(robot_frames[4])
        self.j_6 = convert_to_xyz_tuple(robot_frames[5])
        self.j_7 = convert_to_xyz_tuple(robot_frames[6])

        self.theta_0 = origin_t_1[3]
        self.theta_1 = act_states_t_1.theta_1
        self.theta_2 = act_states_t_1.theta_2
        self.theta_3 = act_states_t_1.theta_3

    def to_json(self) -> json:
        return json.dumps(self.__dict__)
