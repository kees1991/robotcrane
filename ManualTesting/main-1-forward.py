import numpy as np
from matplotlib import pyplot as plt

from Objects.ActuatorStates import ActuatorStates
from Objects.Pose import Pose
from Objects.RobotCrane import RobotCrane

import matplotlib.animation as animation

from Objects.Trajectory import Trajectory
from Tooling.Plotting import setup_animation_axes_3d, animate_3d
from Tooling.plot_tools import plot_robot, plot_trajectory
import matplotlib
matplotlib.use('TkAgg')

if __name__ == '__main__':
    robot = RobotCrane()

    # Next pose actuator states
    d_1 = 0.7
    theta_1 = np.deg2rad(0)
    theta_2 = np.deg2rad(0)
    theta_3 = np.deg2rad(0)
    l_6 = 0.6

    # Set the next pose on the robot
    states = ActuatorStates(d_1, theta_1, theta_2, theta_3, l_6)
    robot.set_act_states_t_1(states)

    print(Pose(robot).to_json())

    plot_robot(robot)
    plt.show()

    # Create the trajectory
    traj = Trajectory(robot, 1/30)
    act_state_time_series = traj.calculate_trajectory()
    traj.t = 0
    plot_trajectory(traj.get_act_state_time_series())
    plt.show()

    print("Robot will move in {} s".format(round(traj.min_move_time, 2)))

    # Create animation
    fig, ax, joint_lines, trajectory_line = setup_animation_axes_3d()
    ani = animation.FuncAnimation(fig, animate_3d, len(act_state_time_series),
                                  fargs=(
                                      act_state_time_series, robot, joint_lines, trajectory_line),
                                  interval=25, blit=True)

    ani.save('robot-crane-forward.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
