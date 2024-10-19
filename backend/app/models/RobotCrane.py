from backend.app.models.Dimensions import Dimensions
from backend.app.services.tools.KinematicsHelper import *


class RobotCrane(object):

    def __init__(self):
        # Robot dimensions
        self.__dimensions = Dimensions(1.0, 0.4, 0.4, -0.2, 0.1, 0.1)

        # Robot limits (maximum positions, velocities, and accelerations)
        self.__min_angle = np.deg2rad(-360)
        self.__max_angle = np.deg2rad(360)
        self.__min_theta_2 = np.deg2rad(-150)
        self.__max_theta_2 = np.deg2rad(150)

        self.max_vel = 0.7
        self.max_acc = 0.7
        self.max_ang_vel = 0.7
        self.max_ang_acc = 0.7

        # Initial origin and next origin
        self.origin_t_0 = (0, 0, 0, np.deg2rad(0))
        self.origin_t_1 = (0, 0, 0, np.deg2rad(0))

        # Initial pose and next pose
        self.act_states_t_0 = ActuatorStates(0.7, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 0.1)
        self.act_states_t_1 = ActuatorStates(0.7, np.deg2rad(0), np.deg2rad(0), np.deg2rad(0), 0.1)

    @property
    def denavit_hartenberg_parameters(self) -> np.ndarray:
        return calculate_dh_parameters(self.__dimensions.l_2, self.__dimensions.l_3, self.__dimensions.d_4,
                                       self.__dimensions.l_5, self.act_states_t_1)

    @property
    def transformation_matrices(self) -> np.ndarray:
        return calculate_transformation_matrices(self.denavit_hartenberg_parameters, self.origin_translation_matrix)

    @property
    def origin_translation_matrix(self) -> np.ndarray:
        return calculate_origin_translation_matrix(self.origin_t_1)

    def set_origin_t_1(self, origin: tuple) -> None:
        self.origin_t_1 = origin

    def set_act_states_t_0(self, act_states: ActuatorStates) -> None:
        self.act_states_t_0 = act_states

    def set_act_states_t_1(self, act_states: ActuatorStates) -> None:
        self.validate_act_states(act_states)
        self.act_states_t_1 = act_states

    def validate_act_states(self, act_states: ActuatorStates) -> None:
        """Validate actuator states according to robot dimensions"""

        # Lift height should not be greater than base column length
        # or smaller than the wrist extensions
        if not (abs(self.__dimensions.d_4) <= act_states.d_1 <= self.__dimensions.l_1):
            raise ValueError("Position out of reach: D1 is out of bounds")

        # Swing angle should not be greater than +- 360 degrees
        if not (self.__min_angle <= act_states.theta_1 <= self.__max_angle):
            raise ValueError("Position out of reach: Theta 1 is out of bounds")

        # Elbow angle should not be greater than +- 150 degrees,
        # to avoid the lower arm clashing with the upper arm
        if not (self.__min_theta_2 <= act_states.theta_2 <= self.__max_theta_2):
            raise ValueError("Position out of reach: Theta 2 is out of bounds")

        # Wrist angle should not be greater than +- 360 degrees
        if not (self.__min_angle <= act_states.theta_1 <= self.__max_angle):
            raise ValueError("Position out of reach: Theta 3 is out of bounds")

        # Jaw extensions should not be greater than the max jaw extensions
        if not (-self.__dimensions.l_7 <= act_states.l_6 <= self.__dimensions.l_7):
            raise ValueError("Position out of reach: L6 is out of bounds")

    def get_dimensions(self) -> Dimensions:
        return self.__dimensions

    def get_x_position(self) -> float:
        """Get the x position of the robot end effector"""
        return self.get_frames()[-1][0][3].item()

    def get_y_position(self) -> float:
        """Get the y position of the robot end effector"""
        return self.get_frames()[-1][1][3].item()

    def get_z_position(self) -> float:
        """Get the z position of the robot end effector"""
        return self.get_frames()[-1][2][3].item()

    def get_phi(self) -> float:
        """Get the rotation of the robot end effector"""
        return self.origin_t_1[
            3] + self.act_states_t_1.theta_1 + self.act_states_t_1.theta_2 + self.act_states_t_1.theta_3

    def get_frames(self) -> np.ndarray:
        """Get the robot state frames"""
        return np.around(calculate_state_frames(len(self.denavit_hartenberg_parameters), self.transformation_matrices),
                         5)

    def inverse_kinematics(self, x: float, y: float, z: float, phi: float, do_open_gripper=True) -> ActuatorStates:
        """Robot inverse kinematics, including origin translation"""

        phi, x, y, z = translate_desired_end_effector_state_for_new_origin(self.origin_translation_matrix,
                                                                           self.origin_t_1, phi, x, y, z)

        d_1, theta_1, theta_2, theta_3, l_6 = calculate_inverse_kinematics(
            self.__dimensions.l_2, self.__dimensions.l_3, self.__dimensions.d_4, self.__dimensions.l_5,
            do_open_gripper, phi, x, y, z)

        return ActuatorStates(d_1, theta_1, theta_2, theta_3, l_6)

    def reset_velocity_and_acceleration(self) -> None:
        self.act_states_t_1.reset_vel_and_acc()
