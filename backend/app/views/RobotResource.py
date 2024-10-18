import asyncio
from time import time

import numpy as np

from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.services.ControlSimulator import ControlSimulator
from backend.app.models.OriginTrajectory import OriginTrajectory
from backend.app.models.Pose import Pose
from backend.app.models.RobotCrane import RobotCrane
from backend.app.models.Trajectory import Trajectory


class RobotResource(object):
    def __init__(self):
        self.streaming_freq = 20
        self.robot = RobotCrane()

    def get_pose(self):
        return Pose(self.robot.get_frames(), self.robot.origin_t_1, self.robot.act_states_t_1).to_json()

    def set_actuator_states(self, states):
        # Reset actuator states velocity and acceleration to zero
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

        self.robot.set_origin_t_1((x, y, z, phi))
        self.robot.set_act_states_t_1(self.robot.act_states_t_0)
        return "True"

    async def stream_pose(self, websocket):
        """Create robot trajectories and stream the poses"""
        traj = Trajectory(self.robot)
        print(f"Moving time: {traj.mov_time}")

        await stream_pose(self.robot, None, traj, websocket, self.streaming_freq)

    async def stream_pose_new_origin(self, websocket):
        """Create origin and robot trajectories and stream the poses"""
        org_traj = OriginTrajectory(self.robot.origin_t_0, self.robot.origin_t_1)

        traj = Trajectory(self.robot)
        traj.set_mov_time(org_traj.min_move_time)
        print(f"Moving time: {traj.mov_time}")

        await stream_pose(self.robot, org_traj, traj, websocket, self.streaming_freq)

    async def stream_pose_controlled_new_origin(self, websocket):
        """Simulate the origin sensor and control loop and stream the poses"""
        sim = ControlSimulator(self.robot)
        await stream_pose(self.robot, sim, sim, websocket, self.streaming_freq)


async def stream_pose(robot, org_traj, traj, websocket, streaming_freq):
    # TODO split up method for trajectory, trajectory+org_trajectory, controlled
    """Stream robot pose updates to via websocket at a given frequency"""
    start_time_ms = get_current_time_ms()
    last_signal_time_ms = 0

    while True:
        current_time_ms = get_current_time_ms()

        if should_update_pose(current_time_ms, last_signal_time_ms, streaming_freq):
            elapsed_time_in_seconds = (current_time_ms - start_time_ms) / 1000

            # Update the robot's state and pose
            if not update_robot_state(robot, org_traj, traj, elapsed_time_in_seconds):
                print("Ending stream.")
                break

            # Send the pose to the frontend via websocket
            pose = Pose(robot.get_frames(), robot.origin_t_1, robot.act_states_t_1)
            await websocket.send_text(pose.to_json())

            # Yield control to the event loop
            await asyncio.sleep(0)

            # Update the last time a signal was processed
            last_signal_time_ms = current_time_ms


def get_current_time_ms() -> int:
    """Return the current time in milliseconds."""
    return round(time() * 1000)


def should_update_pose(current_time_ms: int, last_signal_time_ms: int, streaming_freq: float) -> bool:
    """Check if enough time has passed to update the pose."""
    return (current_time_ms - last_signal_time_ms) >= (1 / streaming_freq) * 1000


def update_robot_state(robot, org_traj, traj, elapsed_time_in_seconds: float) -> bool:
    """
    Update the robot's origin and actuator states based on the trajectory.
    """
    # Update robot origin
    next_origin = get_next_origin(robot, org_traj, elapsed_time_in_seconds)
    if next_origin is None:
        print("No next origin found.")
        return False
    robot.set_origin_t_1(next_origin)

    # Update actuator state
    next_act_state = traj.next_step(elapsed_time_in_seconds)
    if next_act_state is None:
        print("No next actuator state found.")
        return False
    robot.set_act_states_t_1(next_act_state)

    return True


def get_next_origin(robot, org_traj, elapsed_time: float):
    """
    Get the next origin step based on the trajectory, if applicable
    """
    if org_traj:
        return org_traj.origin_next_step(elapsed_time)
    return robot.origin_t_0

