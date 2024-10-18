from backend.app.services.tools.TrajectoryHelper import *


class OriginTrajectory(object):
    """Defining a trajectory for the robot origin"""

    def __init__(self,
                 origin_t_0: tuple, origin_t_1: tuple,
                 max_vel: float = 0.1, max_acc: float = 0.1,
                 max_ang_vel: float = 0.1, max_ang_acc: float = 0.1):
        self.origin_t_0 = origin_t_0
        self.origin_t_1 = origin_t_1

        self.max_vel = max_vel
        self.max_acc = max_acc
        self.max_ang_vel = max_ang_vel
        self.max_ang_acc = max_ang_acc

        self.__moving_time = self.min_move_time

    @property
    def min_move_time(self) -> float:
        t_min_org_x = calculate_minimum_move_time(self.max_vel, self.max_acc, self.origin_t_0[0], self.origin_t_1[0])
        t_min_org_y = calculate_minimum_move_time(self.max_vel, self.max_acc, self.origin_t_0[1], self.origin_t_1[1])
        t_min_org_z = calculate_minimum_move_time(self.max_vel, self.max_acc, self.origin_t_0[2], self.origin_t_1[2])
        t_min_org_phi = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.origin_t_0[3],
                                                    self.origin_t_1[3])

        return max(t_min_org_x, t_min_org_y, t_min_org_z, t_min_org_phi)

    @property
    def x_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[0], self.origin_t_1[0], 0, self.min_move_time)

    @property
    def y_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[1], self.origin_t_1[1], 0, self.min_move_time)

    @property
    def z_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[2], self.origin_t_1[2], 0, self.min_move_time)

    @property
    def phi_coefficients(self) -> Tuple[float, float, float, float]:
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[3], self.origin_t_1[3], 0, self.min_move_time)

    def get_moving_time(self) -> float:
        return self.__moving_time

    def next_step(self, t: float) -> None | tuple:
        if t >= self.__moving_time:
            return None

        return self.calculate_next_step(t)

    def calculate_next_step(self, t: float) -> Tuple[float, float, float, float]:
        org_x = calculate_position(*self.x_coefficients, t)
        org_y = calculate_position(*self.y_coefficients, t)
        org_z = calculate_position(*self.z_coefficients, t)
        org_phi = calculate_position(*self.phi_coefficients, t)

        return org_x, org_y, org_z, org_phi
