import numpy as np

from backend.app.models.RobotCrane import RobotCrane
from backend.app.services.tools.plotting import plot_robot

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

if __name__ == '__main__':
    """Test robot new origin and IK at new origin"""
    robot = RobotCrane()

    # Move end-effector to desired position and orientation
    x = 0.4
    y = 0.4
    z = 0.5
    phi = np.deg2rad(90)

    act_states = robot.inverse_kinematics(x, y, z, phi)
    robot.set_act_states_t_1(act_states)

    # Plot robot at initial origin
    fs = robot.get_frames()
    print(f"End-frame \n{fs[-1]}")
    plot_robot(robot)

    # Plot robot at new origin
    robot.set_new_origin((0.25, 0.25, 0.2, np.deg2rad(45)))
    fs_new = robot.get_frames()
    print(f"End-frame after new origin\n{fs_new[-1]}")
    plot_robot(robot)

    # Plot robot at new origin after moving end-effector to desired position and orientation
    act_states = robot.inverse_kinematics(x, y, z, phi)
    robot.set_act_states_t_1(act_states)
    fs_2 = robot.get_frames()
    print(f"End-frame after IK at new origin\n{fs_2[-1]}")
    plot_robot(robot)

    plt.show()
