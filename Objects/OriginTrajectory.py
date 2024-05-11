from matplotlib import pyplot as plt

from Tooling.trajectory import calculate_minimum_move_time, get_coefficients_nonzero_v_and_a, calculate_position


class OriginTrajectory(object):

    def __init__(self, origin_t_0, origin_t_1, max_vel=0.1, max_acc=0.1, max_ang_vel=0.1, max_ang_acc=0.1,
                 time_step_size=0.1):
        self.origin_t_0 = origin_t_0
        self.origin_t_1 = origin_t_1

        self.max_vel = max_vel
        self.max_acc = max_acc
        self.max_ang_vel = max_ang_vel
        self.max_ang_acc = max_ang_acc

        self.time_step_size = time_step_size

        self.org_time_series = None

        self.t = 0

        self.mov_time = self.min_move_time

    def set_mov_time(self, mov_time):
        self.mov_time = mov_time

    @property
    def min_move_time(self):
        t_min_org_x = calculate_minimum_move_time(self.max_vel, self.max_acc, self.origin_t_0[0], self.origin_t_1[0])
        t_min_org_y = calculate_minimum_move_time(self.max_vel, self.max_acc, self.origin_t_0[1], self.origin_t_1[1])
        t_min_org_z = calculate_minimum_move_time(self.max_vel, self.max_acc, self.origin_t_0[2], self.origin_t_1[2])
        t_min_org_phi = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.origin_t_0[3],
                                                    self.origin_t_1[3])

        return max(t_min_org_x, t_min_org_y, t_min_org_z, t_min_org_phi)

    @property
    def x_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[0], self.origin_t_1[0], 0, self.min_move_time)

    @property
    def y_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[1], self.origin_t_1[1], 0, self.min_move_time)

    @property
    def z_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[2], self.origin_t_1[2], 0, self.min_move_time)

    @property
    def phi_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.origin_t_0[3], self.origin_t_1[3], 0, self.min_move_time)

    def calculate_trajectory(self):
        origin_time_series = []

        while self.t <= self.min_move_time:
            origin_time_series.append(self.origin_next_step())

        self.org_time_series = origin_time_series
        return self.org_time_series

    def origin_next_step_real_time(self, t):
        if t >= self.mov_time:
            return None

        org_x, org_y, org_z, org_phi = self.next_step(t)

        return [org_x, org_y, org_z, org_phi]

    def origin_next_step(self):
        if self.t >= self.min_move_time:
            return [*self.origin_t_1]

        org_x, org_y, org_z, org_phi = self.next_step(self.t)

        self.t += self.time_step_size

        return [org_x, org_y, org_z, org_phi]

    def next_step(self, t):
        a_0_org_x, a_1_org_x, a_2_org_x, a_3_org_x = self.x_coefficients
        a_0_org_y, a_1_org_y, a_2_org_y, a_3_org_y = self.y_coefficients
        a_0_org_z, a_1_org_z, a_2_org_z, a_3_org_z = self.z_coefficients
        a_0_org_phi, a_1_org_phi, a_2_org_phi, a_3_org_phi = self.phi_coefficients

        org_x = calculate_position(a_0_org_x, a_1_org_x, a_2_org_x, a_3_org_x, t)
        org_y = calculate_position(a_0_org_y, a_1_org_y, a_2_org_y, a_3_org_y, t)
        org_z = calculate_position(a_0_org_z, a_1_org_z, a_2_org_z, a_3_org_z, t)
        org_phi = calculate_position(a_0_org_phi, a_1_org_phi, a_2_org_phi, a_3_org_phi, t)

        return org_x, org_y, org_z, org_phi
