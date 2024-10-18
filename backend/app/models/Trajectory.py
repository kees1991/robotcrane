from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.models.RobotCrane import RobotCrane
from backend.app.services.tools.TrajectoryHelper import *


class Trajectory(object):
    """Defining a trajectory for the robot"""

    def __init__(self, act_states_t_0: ActuatorStates, act_states_t_1: ActuatorStates, max_vel: float, max_acc: float,
                 max_ang_vel: float, max_ang_acc: float):
        self.act_states_t_0 = act_states_t_0
        self.act_states_t_1 = act_states_t_1

        self.max_vel = max_vel
        self.max_acc = max_acc
        self.max_ang_vel = max_ang_vel
        self.max_ang_acc = max_ang_acc

        self.__moving_time = self.min_move_time

    @property
    def min_move_time(self) -> float:
        t_min_d_1 = calculate_minimum_move_time(self.max_vel, self.max_acc, self.act_states_t_0.d_1,
                                                self.act_states_t_1.d_1)
        t_min_theta_1 = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.act_states_t_0.theta_1,
                                                    self.act_states_t_1.theta_1)
        t_min_theta_2 = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.act_states_t_0.theta_2,
                                                    self.act_states_t_1.theta_2)
        t_min_theta_3 = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.act_states_t_0.theta_3,
                                                    self.act_states_t_1.theta_3)
        t_min_l_6 = calculate_minimum_move_time(self.max_vel, self.max_acc, self.act_states_t_0.l_6,
                                                self.act_states_t_1.l_6)

        return max(t_min_d_1, t_min_theta_1, t_min_theta_2, t_min_theta_3, t_min_l_6)

    @property
    def d_1_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.d_1, self.act_states_t_1.d_1,
                                                self.act_states_t_0.d_1_v, self.__moving_time)

    @property
    def theta_1_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.theta_1, self.act_states_t_1.theta_1,
                                                self.act_states_t_0.theta_1_v, self.__moving_time)

    @property
    def theta_2_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.theta_2, self.act_states_t_1.theta_2,
                                                self.act_states_t_0.theta_2_v, self.__moving_time)

    @property
    def theta_3_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.theta_3, self.act_states_t_1.theta_3,
                                                self.act_states_t_0.theta_3_v, self.__moving_time)

    @property
    def l_6_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.l_6, self.act_states_t_1.l_6,
                                                self.act_states_t_0.l_6_v, self.__moving_time)

    def set_moving_time(self, time: float) -> None:
        self.__moving_time = time

    def get_moving_time(self) -> float:
        return self.__moving_time

    def next_step(self, t: float) -> ActuatorStates | None:
        if t >= self.__moving_time:
            return None

        return self.calculate_next_step(t)

    def calculate_next_step(self, t: float) -> ActuatorStates:
        a_0_d_1, a_1_d_1, a_2_d_1, a_3_d_1 = self.d_1_coefficients
        a_0_t_1, a_1_t_1, a_2_t_1, a_3_t_1 = self.theta_1_coefficients
        a_0_t_2, a_1_t_2, a_2_t_2, a_3_t_2 = self.theta_2_coefficients
        a_0_t_3, a_1_t_3, a_2_t_3, a_3_t_3 = self.theta_3_coefficients
        a_0_l_6, a_1_l_6, a_2_l_6, a_3_l_6 = self.l_6_coefficients

        d_1 = calculate_position(a_0_d_1, a_1_d_1, a_2_d_1, a_3_d_1, t)
        d_1_v = calculate_velocity(a_1_d_1, a_2_d_1, a_3_d_1, t)
        d_1_a = calculate_acceleration(a_2_d_1, a_3_d_1, t)

        t_1 = calculate_position(a_0_t_1, a_1_t_1, a_2_t_1, a_3_t_1, t)
        t_1_v = calculate_velocity(a_1_t_1, a_2_t_1, a_3_t_1, t)
        t_1_a = calculate_acceleration(a_2_t_1, a_3_t_1, t)

        t_2 = calculate_position(a_0_t_2, a_1_t_2, a_2_t_2, a_3_t_2, t)
        t_2_v = calculate_velocity(a_1_t_2, a_2_t_2, a_3_t_2, t)
        t_2_a = calculate_acceleration(a_2_t_2, a_3_t_2, t)

        t_3 = calculate_position(a_0_t_3, a_1_t_3, a_2_t_3, a_3_t_3, t)
        t_3_v = calculate_velocity(a_1_t_3, a_2_t_3, a_3_t_3, t)
        t_3_a = calculate_acceleration(a_2_t_3, a_3_t_3, t)

        l_6 = calculate_position(a_0_l_6, a_1_l_6, a_2_l_6, a_3_l_6, t)
        l_6_v = calculate_velocity(a_1_l_6, a_2_l_6, a_3_l_6, t)
        l_6_a = calculate_acceleration(a_2_l_6, a_3_l_6, t)

        return ActuatorStates(
            d_1, t_1, t_2, t_3, l_6,
            d_1_v, t_1_v, t_2_v, t_3_v, l_6_v,
            d_1_a, t_1_a, t_2_a, t_3_a, l_6_a)
