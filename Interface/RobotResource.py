import json
from time import time

import numpy as np

from Objects.ActuatorStates import ActuatorStates
from Objects.ControlSimulator import ControlSimulator
from Objects.OriginTrajectory import OriginTrajectory
from Objects.Pose import Pose
from Objects.RobotCrane import RobotCrane
from Objects.Trajectory import Trajectory


class RobotResource(object):
    def __init__(self):
        self.streaming_freq = 20  # Hz
        self.robot = RobotCrane()
        self.robot.set_act_states_t_1(ActuatorStates(0.7, 0, 0, 0, 0.1))
        self.robot.set_new_origin((0, 0, 0, 0))

    def get_robot_dimensions(self):
        dimensions = {
            "l_1": self.robot.l_1,
            "l_2": self.robot.l_2,
            "l_3": self.robot.l_3,
            "d_4": self.robot.d_4,
            "l_5": self.robot.l_5,
            "l_7": self.robot.l_7
        }
        return json.dumps(dimensions)

    def get_pose(self):
        return Pose(self.robot).to_json()

    def set_actuator_states(self, states):
        if self.robot.act_states_t_1 is not None:
            old_states = self.robot.act_states_t_1
            old_states.reset_vel_and_acc()
            self.robot.set_act_states_t_0(old_states)

        # Convert degrees to radians
        act_states = ActuatorStates(
            states["d_1"],
            np.deg2rad(states["theta_1"]),
            np.deg2rad(states["theta_2"]),
            np.deg2rad(states["theta_3"]),
            states["l_6"]
        )
        self.robot.set_act_states_t_1(act_states)

        return "True"

    def set_end_effectors(self, desired_position):
        x, y, z = desired_position["x"], desired_position["y"], desired_position["z"]
        phi = np.deg2rad(desired_position["phi"])
        do_open_gripper = desired_position["doOpenGripper"]

        act_states = self.robot.inverse_kinematics(x, y, z, phi, do_open_gripper)
        self.robot.set_act_states_t_1(act_states)
        return "True"

    def set_new_origin(self, desired_org_position):
        x, y, z = desired_org_position["x"], desired_org_position["y"], desired_org_position["z"]
        phi = np.deg2rad(desired_org_position["phi"])

        # Move the origin
        self.robot.set_new_origin((x, y, z, phi))
        self.robot.set_act_states_t_1(self.robot.act_states_t_0)

        return "True"

    async def stream_pose(self, websocket):
        # Create the robot trajectory
        traj = Trajectory(self.robot, 0.1)
        print("Moving time: {}".format(traj.mov_time))

        await stream_pose(self.robot, None, traj, websocket, self.streaming_freq)

    async def stream_pose_new_origin(self, websocket):
        # Create the origin trajectory
        org_traj = OriginTrajectory(self.robot.origin_t_0, self.robot.origin_t_1)

        # Create the robot trajectory
        traj = Trajectory(self.robot, 0.1)
        traj.set_mov_time(org_traj.min_move_time)
        print("Moving time: {}".format(traj.mov_time))

        await stream_pose(self.robot, org_traj, traj, websocket, self.streaming_freq)

    async def stream_pose_controlled_new_origin(self, websocket):
        sim = ControlSimulator(self.robot)
        await stream_pose(self.robot, sim, sim, websocket, self.streaming_freq)


async def stream_pose(robot, org_traj, traj, websocket, streaming_freq):
    # Calculate the next trajectory step at the current time, and send it to the frontend
    last_milliseconds = 0
    start_milliseconds = round(time() * 1000)

    while True:
        milliseconds = round(time() * 1000)
        if milliseconds - last_milliseconds >= (1/streaming_freq) * 1000:
            seconds_since_start = (milliseconds - start_milliseconds) / 1000
            print("Seconds since start: {}".format(seconds_since_start))

            # Update robot origin
            if org_traj is not None:
                next_origin = org_traj.origin_next_step_real_time(seconds_since_start)
            else:
                next_origin = robot.origin_t_0

            if next_origin is None:
                print("Breaking loop")
                break
            robot.set_new_origin(next_origin)

            # Update the robot actuator state
            next_act_state = traj.trajectory_next_step_real_time(seconds_since_start)
            if next_act_state is None:
                print("Breaking loop")
                break

            robot.set_act_states_t_1(next_act_state)

            # Retrieve the Pose for the Frontend rendering
            pose = Pose(robot)

            # Send the pose over the websocket
            await websocket.send(pose.to_json())
            last_milliseconds = milliseconds
