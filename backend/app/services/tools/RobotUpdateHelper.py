import json
import numpy as np

from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.models.Pose import Pose
from backend.app.models.RobotCrane import RobotCrane


def set_actuator_states(robot: RobotCrane, states: json) -> str:
    act_states = convert_json_to_actuator_states(states)
    robot.set_act_states_t_1(act_states)

    return "True"


def convert_json_to_actuator_states(act_json: json) -> ActuatorStates:
    # Convert degrees to radians
    act_states = ActuatorStates(
        act_json["d_1"],
        np.deg2rad(act_json["theta_1"]),
        np.deg2rad(act_json["theta_2"]),
        np.deg2rad(act_json["theta_3"]),
        act_json["l_6"]
    )
    return act_states


def set_end_effectors(robot: RobotCrane, desired_position: json) -> str:
    x, y, z, phi = convert_json_to_end_effector_position(desired_position)
    do_open_gripper = bool(desired_position["doOpenGripper"])

    actuator_states = robot.inverse_kinematics(x, y, z, phi, do_open_gripper)
    robot.set_act_states_t_1(actuator_states)
    return "True"


def set_new_origin(robot: RobotCrane, desired_origin_position: json) -> str:
    x, y, z, phi = convert_json_to_end_effector_position(desired_origin_position)

    robot.set_origin_t_1((x, y, z, phi))
    return "True"


def convert_json_to_end_effector_position(pos_json: json) -> tuple[float, float, float, float]:
    x, y, z = float(pos_json["x"]), float(pos_json["y"]), float(pos_json["z"])
    phi = float(np.deg2rad(pos_json["phi"]))

    return x, y, z, phi


def get_pose(robot: RobotCrane) -> json:
    return Pose(robot.get_frames(), robot.origin_t_1, robot.act_states_t_1).to_json()
