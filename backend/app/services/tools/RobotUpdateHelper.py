import json
import numpy as np

from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.models.Pose import Pose
from backend.app.models.RobotCrane import RobotCrane


def initialize_robot(robot: RobotCrane) -> dict:
    dimensions = robot.get_dimensions()
    pose = Pose(robot.get_frames(), robot.origin_t_1, robot.act_states_t_1)

    return {"init_robot_data": {"dimensions": dimensions.__dict__, "pose": pose.__dict__}}


def get_pose(robot: RobotCrane) -> dict:
    pose = Pose(robot.get_frames(), robot.origin_t_1, robot.act_states_t_1)
    return {"pose_data": pose.__dict__}


def set_actuator_states(robot: RobotCrane, states: json) -> None:
    act_states = convert_json_to_actuator_states(states)
    robot.set_act_states_t_1(act_states)


def convert_json_to_actuator_states(act_json: json) -> ActuatorStates:
    # Convert degrees to radians
    act_states = ActuatorStates(
        act_json["d1"],
        np.deg2rad(act_json["theta1"]),
        np.deg2rad(act_json["theta2"]),
        np.deg2rad(act_json["theta3"]),
        act_json["l6"]
    )
    return act_states


def set_end_effectors(robot: RobotCrane, desired_position: json) -> None:
    x, y, z, phi = convert_json_to_end_effector_position(desired_position)
    do_open_gripper = bool(desired_position["doOpenGripper"])

    actuator_states = robot.inverse_kinematics(x, y, z, phi, do_open_gripper)
    robot.set_act_states_t_1(actuator_states)


def set_new_origin(robot: RobotCrane, desired_origin_position: json) -> None:
    x, y, z, phi = convert_json_to_end_effector_position(desired_origin_position)

    robot.set_origin_t_1((x, y, z, phi))


def convert_json_to_end_effector_position(pos_json: json) -> tuple[float, float, float, float]:
    x, y, z = float(pos_json["x"]), float(pos_json["y"]), float(pos_json["z"])
    phi = float(np.deg2rad(pos_json["phi"]))

    return x, y, z, phi
