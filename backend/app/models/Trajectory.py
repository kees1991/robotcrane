from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.services.tools.TrajectoryBuilder import calculate_minimum_move_time, get_coefficients_nonzero_v_and_a, calculate_position, \
    calculate_velocity, calculate_acceleration


class Trajectory(object):
    """Defining a trajectory for the robot"""

    def __init__(self, robot, time_step_size=0.1):
        self.act_states_t_0 = robot.act_states_t_0
        self.act_states_t_1 = robot.act_states_t_1
        self.max_vel = robot.max_vel
        self.max_acc = robot.max_acc
        self.max_ang_vel = robot.max_ang_vel
        self.max_ang_acc = robot.max_ang_acc

        self.time_step_size = time_step_size

        self.next_act_state = None
        self.act_state_time_series = None

        self.t = 0

        self.mov_time = self.min_move_time

    def set_mov_time(self, mov_time):
        self.mov_time = mov_time

    @property
    def min_move_time(self):
        t_min_d_1 = calculate_minimum_move_time(self.max_vel, self.max_acc, self.act_states_t_0.d_1, self.act_states_t_1.d_1)
        t_min_theta_1 = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.act_states_t_0.theta_1, self.act_states_t_1.theta_1)
        t_min_theta_2 = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.act_states_t_0.theta_2, self.act_states_t_1.theta_2)
        t_min_theta_3 = calculate_minimum_move_time(self.max_ang_vel, self.max_ang_acc, self.act_states_t_0.theta_3, self.act_states_t_1.theta_3)
        t_min_l_6 = calculate_minimum_move_time(self.max_vel, self.max_acc, self.act_states_t_0.l_6, self.act_states_t_1.l_6)

        return max(t_min_d_1, t_min_theta_1, t_min_theta_2, t_min_theta_3, t_min_l_6)

    @property
    def d_1_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.d_1, self.act_states_t_1.d_1, self.act_states_t_0.d_1_v, self.mov_time)

    @property
    def theta_1_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.theta_1, self.act_states_t_1.theta_1, self.act_states_t_0.theta_1_v, self.mov_time)

    @property
    def theta_2_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.theta_2, self.act_states_t_1.theta_2, self.act_states_t_0.theta_2_v, self.mov_time)

    @property
    def theta_3_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.theta_3, self.act_states_t_1.theta_3, self.act_states_t_0.theta_3_v, self.mov_time)

    @property
    def l_6_coefficients(self):
        return get_coefficients_nonzero_v_and_a(self.act_states_t_0.l_6, self.act_states_t_1.l_6, self.act_states_t_0.l_6_v, self.mov_time)

    def get_act_state_time_series(self):
        if self.act_state_time_series is None:
            self.act_state_time_series = self.calculate_trajectory()

        return self.act_state_time_series

    def calculate_trajectory(self):
        act_state_time_series = []

        if self.mov_time == 0:
            return act_state_time_series

        while self.t <= self.mov_time:
            act_state_time_series.append(self.trajectory_next_step())

        return act_state_time_series

    def trajectory_next_step_real_time(self, t):
        if t >= self.mov_time:
            return None

        self.next_step(t)

        return self.next_act_state

    def trajectory_next_step(self):
        if self.t >= self.mov_time:
            return self.next_act_state

        self.next_step(self.t)

        self.t += self.time_step_size

        return self.next_act_state

    def next_step(self, t):
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

        self.next_act_state = ActuatorStates(d_1, t_1, t_2, t_3, l_6, d_1_v, t_1_v, t_2_v, t_3_v, l_6_v, d_1_a, t_1_a,
                                             t_2_a, t_3_a, l_6_a)
