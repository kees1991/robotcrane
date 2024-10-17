import numpy as np

from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.services.tools.KinematicsHelper import calculate_state_frames, calculate_transformation_matrices, \
    calculate_dh_parameters, calculate_origin_translation_matrix


class RobotCrane(object):

    def __init__(self):
        # Robot dimensions
        self.l_1 = 1  # base column length
        self.l_2 = 0.4  # upper arm length
        self.l_3 = 0.4  # lower arm length
        self.d_4 = -0.2  # wrist extension length
        self.l_5 = 0.1  # gripper length
        self.l_7 = 0.1  # maximum jaw extension length

        # Max positions
        self.min_angle = np.deg2rad(-360)
        self.max_angle = np.deg2rad(360)
        self.min_theta_2 = np.deg2rad(-150)
        self.max_theta_2 = np.deg2rad(150)

        # Max velocity and max acceleration
        self.max_vel = 0.7
        self.max_acc = 0.7
        self.max_ang_vel = 0.7
        self.max_ang_acc = 0.7

        # Initial origin and next origin
        self.origin_t_0 = (0, 0, 0, np.deg2rad(0))
        self.origin_t_1 = (0, 0, 0, np.deg2rad(0))

        # Origin translation matrix
        self.T_origin = np.identity(4)

        # Initial pose and next pose
        self.act_states_t_0 = ActuatorStates(0.7, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 0.1)
        self.act_states_t_1 = ActuatorStates(0.7, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 0.1)

    @property
    def dh_params(self):
        """Calculate the Denavit-Hartenberg parameters"""
        return calculate_dh_parameters(self.l_2, self.l_3, self.d_4, self.l_5, self.act_states_t_1)

    @property
    def t_matrices(self):
        """Calculate the transformation matrices"""
        return calculate_transformation_matrices(self.dh_params, len(self.dh_params), self.T_origin)

    def set_act_states_t_0(self, act_states):
        self.act_states_t_0 = act_states

    def set_act_states_t_1(self, act_states):
        self.validate_act_states(act_states)
        self.act_states_t_1 = act_states

    def validate_act_states(self, act_states):
        """Validate actuator states according to robot dimensions"""

        # Lift height should not be greater than base column length
        # or smaller than the wrist extensions
        if not (abs(self.d_4) <= act_states.d_1 <= self.l_1):
            raise ValueError("Position out of reach: D1 is out of bounds")

        # Swing angle should not be greater than +- 360 degrees
        if not (self.min_angle <= act_states.theta_1 <= self.max_angle):
            raise ValueError("Position out of reach: Theta 1 is out of bounds")

        # Elbow angle should not be greater than +- 150 degrees,
        # to avoid the lower arm clashing with the upper arm
        if not (self.min_theta_2 <= act_states.theta_2 <= self.max_theta_2):
            raise ValueError("Position out of reach: Theta 2 is out of bounds")

        # Wrist angle should not be greater than +- 360 degrees
        if not (self.min_angle <= act_states.theta_1 <= self.max_angle):
            raise ValueError("Position out of reach: Theta 3 is out of bounds")

        # Jaw extensions should not be greater than the max jaw extensions
        if not (-self.l_7 <= act_states.l_6 <= self.l_7):
            raise ValueError("Position out of reach: L6 is out of bounds")

    def get_x_position(self):
        """Get the x position of the robot end effector"""
        return self.get_frames()[-1][0][3]

    def get_y_position(self):
        """Get the y position of the robot end effector"""
        return self.get_frames()[-1][1][3]

    def get_z_position(self):
        """Get the z position of the robot end effector"""
        return self.get_frames()[-1][2][3]

    def get_phi(self):
        """Get the rotation of the robot end effector"""
        return self.origin_t_1[3] + self.act_states_t_1.theta_1 + self.act_states_t_1.theta_2 + self.act_states_t_1.theta_3

    def get_frames(self):
        """Get the robot state frames"""
        return np.around(calculate_state_frames(len(self.dh_params), self.t_matrices), 5)

    def inverse_kinematics(self, x, y, z, phi, do_open_gripper=True):
        """Robot inverse kinematics, including origin translation"""
        # Translate goal wrt new origin
        translated_goal = np.dot(self.T_origin, np.array([x, y, z, 1]))
        x, y, z = translated_goal[0], translated_goal[1], translated_goal[2]

        if self.origin_t_1 is not None:
            phi -= self.origin_t_1[3]

        # For IK we assume that gripper will be open or closed
        if do_open_gripper:
            l_6 = 0.1
        else:
            l_6 = 0.0

        g_x = x - l_6 * np.cos(phi)
        g_y = y - l_6 * np.sin(phi)

        w_x = g_x - self.l_5 * np.cos(phi)
        w_y = g_y - self.l_5 * np.sin(phi)

        c_2 = (w_x ** 2 + w_y ** 2 - self.l_2 ** 2 - self.l_3 ** 2) / (2 * self.l_2 * self.l_3)
        if c_2 > 1:
            print(f"Cos of theta 2 is {c_2}, while it cannot be larger than 1")
            raise ValueError("Given end-effector position is out of reach")

        # Other solution: - np.sqrt(1 - c_2 ** 2)
        s_2 = np.sqrt(1 - c_2 ** 2)

        theta_2 = np.arctan2(s_2, c_2)

        k_1 = self.l_2 + self.l_3 * (np.cos(theta_2))
        k_2 = self.l_3 * (np.sin(theta_2))
        theta_1 = np.arctan2(w_y, w_x) - np.arctan2(k_2, k_1)

        theta_3 = phi - theta_1 - theta_2

        d_1 = z - self.d_4

        return ActuatorStates(d_1, theta_1, theta_2, theta_3, l_6)

    def set_new_origin(self, new_origin):
        """Set new origin and update the origin translation matrix"""
        self.origin_t_1 = new_origin

        self.T_origin = calculate_origin_translation_matrix(new_origin)
