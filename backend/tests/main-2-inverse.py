import numpy as np
from matplotlib import pyplot as plt

from backend.app.models.Pose import Pose
from backend.app.models.Trajectory import Trajectory
from backend.app.services.tools import plotting
from backend.app.services.tools.animation import setup_animation_axes_3d, animate_3d
from backend.app.services.tools.plotting import plot_robot
from backend.app.models.RobotCrane import RobotCrane

import matplotlib.animation as animation
import matplotlib

matplotlib.use('TkAgg')

if __name__ == '__main__':
    """Test robot inverse kinematics"""
    robot = RobotCrane()

    # Desired end-effector position and Z-axis orientation
    x = 0.4
    y = 0.4
    z = 0.5
    phi = np.deg2rad(0)

    # Use Inverse kinematics to calculate the actuator states
    act_states = robot.inverse_kinematics(x, y, z, phi, True)
    robot.set_act_states_t_1(act_states)

    print(f"Robot pose: {Pose(robot).to_json()}")

    plot_robot(robot)
    plt.show()

    # Create the trajectory
    traj = Trajectory(robot, 1 / 30)
    act_state_time_series = traj.calculate_trajectory()
    print(f"Robot will move in {round(traj.min_move_time, 2)} s")

    traj.t = 0
    plotting.plot_trajectory(traj.get_act_state_time_series())
    plt.show()

    fig, ax, joint_lines, trajectory_line = setup_animation_axes_3d()
    ani = animation.FuncAnimation(fig, animate_3d, len(act_state_time_series),
                                  fargs=(
                                      act_state_time_series, robot, joint_lines, trajectory_line),
                                  interval=25, blit=True)

    ani.save('robot-crane-inverse.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
