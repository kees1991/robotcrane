import asyncio
from time import time

from fastapi import WebSocket

from backend.app.models.OriginTrajectory import OriginTrajectory
from backend.app.models.Pose import Pose
from backend.app.models.RobotCrane import RobotCrane
from backend.app.models.Trajectory import Trajectory
from backend.app.services.ControlSimulator import ControlSimulator
from backend.app.views.WebSocketAPI import WebSocketAPI


def get_current_time_ms() -> int:
    """Return the current time in milliseconds."""
    return round(time() * 1000)


def update_robot(robot: RobotCrane, _, trajectory: Trajectory, elapsed_time_in_seconds: float) -> bool:
    next_act_state = trajectory.next_step(elapsed_time_in_seconds)

    if next_act_state is None:
        print("No next actuator state found")
        return False

    robot.set_act_states_t_1(next_act_state)

    return True


def update_robot_with_new_origin(robot: RobotCrane, origin_trajectory: OriginTrajectory, trajectory: Trajectory,
                                 elapsed_time_in_seconds: float) -> bool:
    # Update robot origin
    next_origin = origin_trajectory.origin_next_step(elapsed_time_in_seconds)
    if next_origin is None:
        print("No next origin found, end streaming.")
        return False
    robot.set_origin_t_1(next_origin)

    # Update robot actuator states
    next_act_state = trajectory.next_step(elapsed_time_in_seconds)
    if next_act_state is None:
        print("No next actuator state found, end streaming.")
        return False
    robot.set_act_states_t_1(next_act_state)

    return True


def update_robot_with_new_origin_and_control_end_effector(robot: RobotCrane, origin_trajectory: OriginTrajectory,
                                                          simulator: ControlSimulator,
                                                          elapsed_time_in_seconds: float) -> bool:
    # Get the next origin
    next_origin = origin_trajectory.origin_next_step(elapsed_time_in_seconds)
    if next_origin is None:
        print("No next origin found, end streaming.")
        return False

    # Update robot actuator states
    next_act_state = simulator.next_step(elapsed_time_in_seconds, next_origin)
    if next_act_state is None:
        print("No next actuator state found, end streaming.")
        return False
    robot.set_act_states_t_1(next_act_state)

    return True


class RobotPoseStreamer(object):

    def __init__(self, websocket: WebSocket, websocket_api: WebSocketAPI):
        self.streaming_frequency = 20
        self.last_signal_time_ms = 0
        self.websocket = websocket
        self.websocket_api = websocket_api

    async def stream_poses(self, robot: RobotCrane) -> None:
        trajectory = Trajectory(robot)
        print(f"Moving time: {trajectory.get_moving_time()}")

        await self.stream(robot, None, trajectory, update_robot)

    async def stream_poses_for_new_origin(self, robot: RobotCrane) -> None:
        origin_trajectory = OriginTrajectory(robot.origin_t_0, robot.origin_t_1)

        trajectory = Trajectory(robot)
        trajectory.set_moving_time(origin_trajectory.min_move_time)

        print(f"Moving time: {trajectory.get_moving_time()}")

        await self.stream(robot, origin_trajectory, trajectory, update_robot_with_new_origin)

    async def stream_poses_for_new_origin_and_control_end_effector(self, robot: RobotCrane) -> None:
        new_org = robot.origin_t_1
        robot.set_origin_t_1(robot.origin_t_0)

        org_traj = OriginTrajectory(robot.origin_t_0, new_org)
        print(f"Moving time: {org_traj.get_moving_time()}")

        simulator = ControlSimulator(robot, org_traj.get_moving_time())

        await self.stream(robot, org_traj, simulator, update_robot_with_new_origin_and_control_end_effector)

    async def stream(self, robot: RobotCrane, origin_next_step_provider, next_step_provider, update_function) -> None:

        start_time_ms = get_current_time_ms()
        while True:
            current_time_ms = get_current_time_ms()

            if not self.should_update_pose(current_time_ms):
                continue

            elapsed_time_in_seconds = (current_time_ms - start_time_ms) / 1000
            if not update_function(robot, origin_next_step_provider, next_step_provider, elapsed_time_in_seconds):
                print("End streaming.")
                break

            # Send the pose to the frontend via websocket
            pose = Pose(robot.get_frames(), robot.origin_t_1, robot.act_states_t_1)
            await self.websocket_api.send_message(self.websocket, pose.to_json())

            # Yield control to the event loop
            await asyncio.sleep(0)

            # Update the last time a signal was processed
            self.last_signal_time_ms = current_time_ms

        # Reset last signal time
        self.last_signal_time_ms = 0

    def should_update_pose(self, current_time_ms: int) -> bool:
        """Check if enough time has passed to update the pose."""
        return (current_time_ms - self.last_signal_time_ms) >= (1 / self.streaming_frequency) * 1000
