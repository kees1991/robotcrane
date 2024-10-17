from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.services.tools.KinematicsHelper import *


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
    def denavit_hartenberg_parameters(self):
        return calculate_dh_parameters(self.l_2, self.l_3, self.d_4, self.l_5, self.act_states_t_1)

    @property
    def transformation_matrices(self):
        return calculate_transformation_matrices(self.denavit_hartenberg_parameters, self.T_origin)

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
        return np.around(calculate_state_frames(len(self.denavit_hartenberg_parameters), self.transformation_matrices), 5)

    def inverse_kinematics(self, x, y, z, phi, do_open_gripper=True):
        """Robot inverse kinematics, including origin translation"""

        phi, x, y, z = translate_desired_end_effector_state_for_new_origin(self.T_origin, self.origin_t_1, phi, x, y, z)

        d_1, theta_1, theta_2, theta_3, l_6 = calculate_inverse_kinematics(
            self.l_2, self.l_3, self.d_4, self.l_5, do_open_gripper, phi, x, y, z)

        return ActuatorStates(d_1, theta_1, theta_2, theta_3, l_6)

    def set_new_origin(self, new_origin):
        """Set new origin and update the origin translation matrix"""
        self.origin_t_1 = new_origin

        self.T_origin = calculate_origin_translation_matrix(new_origin)
