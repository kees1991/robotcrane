import numpy as np


def calculate_minimum_move_time(max_velocity, max_acceleration, t0, t1):
    t_based_on_max_v = 3 * (abs(t1 - t0)) / (2 * max_velocity)
    t_based_on_max_a = np.sqrt((6 * abs(t1 - t0)) / max_acceleration)
    return max(t_based_on_max_v, t_based_on_max_a)


def get_coefficients_nonzero_v_and_a(t0, t1, v0, t_end, v1=0):
    a_0 = t0
    a_1 = v0
    a_2 = (3 / t_end ** 2) * (t1 - t0) - (2 / t_end) * v0 - (1 / t_end) * v1
    a_3 = -(2 / t_end ** 3) * (t1 - t0) + (1 / t_end ** 2) * (v1 - v0)

    return a_0, a_1, a_2, a_3


def calculate_position(a_0, a_1, a_2, a_3, t):
    return a_0 + a_1 * t + a_2 * t ** 2 + a_3 * t ** 3


def calculate_velocity(a_1, a_2, a_3, t):
    return a_1 + 2 * a_2 * t + 3 * a_3 * t ** 2


def calculate_acceleration(a_2, a_3, t):
    return 2 * a_2 + 6 * a_3 * t
