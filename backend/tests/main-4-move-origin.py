import numpy as np
import matplotlib.animation as animation
from matplotlib import pyplot as plt

from backend.app.models.OriginTrajectory import OriginTrajectory
from backend.app.models.RobotCrane import RobotCrane
from backend.app.models.Trajectory import Trajectory
from AnimationBuilder import setup_animation_axes_3d, animate_3d_with_origin
from backend.tests.Plotter import plot_robot

import matplotlib
matplotlib.use('TkAgg')

if __name__ == '__main__':
    """Test robot moving to a new origin"""
    robot = RobotCrane()

    # Set a new origin
    robot.set_new_origin((0.0, 0.0, 0.2, np.deg2rad(90)))

    # Keep the robot Actuator states the same
    robot.set_act_states_t_1(robot.act_states_t_0)

    # Plot robot at the new origin
    plot_robot(robot)
    plt.show()

    # Create the origin trajectory
    org_traj = OriginTrajectory(robot.origin_t_0, robot.origin_t_1, max_vel=0.5, max_acc=0.5, max_ang_vel=0.5, max_ang_acc=0.5, time_step_size=1/30)
    org_time_series = org_traj.calculate_trajectory()
    print(f"Origin will move in {round(org_traj.mov_time, 2)} s")

    # Create the robot trajectory
    traj = Trajectory(robot, 1 / 30)
    traj.set_mov_time(org_traj.min_move_time)
    act_state_time_series = traj.calculate_trajectory()
    print(f"Robot will move in {round(traj.mov_time, 2)} s")

    fig, ax, joint_lines, trajectory_line = setup_animation_axes_3d()
    ani = animation.FuncAnimation(fig, animate_3d_with_origin, len(act_state_time_series),
                                  fargs=(
                                      act_state_time_series, org_time_series, robot, joint_lines, trajectory_line),
                                  interval=25, blit=True)
    ani.save('robot-crane-move-origin.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
