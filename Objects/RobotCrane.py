import numpy as np

from Objects.ActuatorStates import ActuatorStates
from Tooling.forwardkinematics import retrieve_frames, calculate_dh_params, retrieve_ts


class RobotCrane(object):

    def __init__(self, base_column_length=1, upper_arm_length=0.4, lower_arm_length=0.4, wrist_ext_length=-0.2,
                 gripper_length=0.1, max_jaw_ext_length=0.1, max_elbow_angle=150):
        # Dimensions
        self.l_1 = base_column_length  # base column length
        self.l_2 = upper_arm_length  # upper arm length
        self.l_3 = lower_arm_length  # lower arm length
        self.d_4 = wrist_ext_length  # wrist extension length
        self.l_5 = gripper_length  # gripper length
        self.l_7 = max_jaw_ext_length  # maximum jaw extension length

        self.min_angle = np.deg2rad(-360)
        self.max_angle = np.deg2rad(360)
        self.min_theta_2 = np.deg2rad(-max_elbow_angle)
        self.max_theta_2 = np.deg2rad(max_elbow_angle)

        # Max velocity and max acceleration
        self.max_vel = 0.7
        self.max_acc = 0.7

        self.max_ang_vel = 0.7
        self.max_ang_acc = 0.7

        self.origin_t_0 = (0, 0, 0, np.deg2rad(0))
        self.origin_t_1 = None

        # Origin translation matrix
        self.T_origin = np.array(
            [
                [1., 0., 0., 0.],
                [0., 1., 0., 0.],
                [0., 0., 1., 0.],
                [0., 0., 0., 1.]
            ]
        )

        # Initial pose
        self.act_states_t_0 = ActuatorStates(0.7, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 0.1)

        # Next pose
        self.act_states_t_1 = None

    @property
    def dh_params(self):
        # Define the Denavit-Hartenberg parameters

        l_2, l_3, d_4, l_5 = self.l_2, self.l_3, self.d_4, self.l_5
        d_1, theta_1, theta_2, theta_3, l_6 = self.act_states_t_1.get_states()

        return np.array(
            [
                [d_1, 0, 0, 0],  # lift
                [0, l_2, 0, theta_1],  # swing rotation and upper arm
                [0, l_3, 0, theta_2],  # elbow rotation and lower arm
                [d_4, 0, 0, theta_3],  # wrist rotation and wrist extension
                [0, l_5, 0, 0],  # fixed jaw
                [0, l_6, 0, 0],  # gripper
            ]
        )

    @property
    def t_matrices(self):
        # Transformation matrices

        return retrieve_ts(self.dh_params, len(self.dh_params), self.T_origin)

    def set_act_states_t_0(self, act_states):
        self.act_states_t_0 = act_states

    def set_act_states_t_1(self, act_states):
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

        self.act_states_t_1 = act_states

    def get_x_position(self):
        return self.get_frames()[-1][0][3]

    def get_y_position(self):
        return self.get_frames()[-1][1][3]

    def get_z_position(self):
        return self.get_frames()[-1][2][3]

    def get_phi(self):
        return self.origin_t_1[3] + self.act_states_t_1.theta_1 + self.act_states_t_1.theta_2 + self.act_states_t_1.theta_3

    # Get the state frames
    def get_frames(self):
        return np.around(retrieve_frames(len(self.dh_params), self.t_matrices), 5)

    def inverse_kinematics(self, x, y, z, phi, do_open_gripper=True):
        # Translate goal wrt new origin
        translated_goal = np.dot(self.T_origin, np.array([x, y, z, 1]))
        x, y, z = translated_goal[0], translated_goal[1], translated_goal[2]

        if self.origin_t_1 is not None:
            phi += self.origin_t_1[3]

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
            print("Cos of theta 2 is {}, while it cannot be larger than 1".format(c_2))
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
        self.origin_t_1 = new_origin

        x, y, z, phi = new_origin[0], new_origin[1], new_origin[2], new_origin[3]
        self.T_origin = np.array(
            [
                [np.cos(phi), np.sin(phi), 0., -x],
                [-np.sin(phi), np.cos(phi), 0., -y],
                [0., 0., 1., -z],
                [0., 0., 0., 1.]
            ]
        )
