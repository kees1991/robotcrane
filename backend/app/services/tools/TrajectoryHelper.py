from typing import Tuple

import numpy as np


def calculate_minimum_move_time(max_velocity: float, max_acceleration: float, t0: float, t1: float) -> float:
    """Calculate minimum moving time, based on max velocity and acceleration"""
    t_based_on_max_v = 3 * (abs(t1 - t0)) / (2 * max_velocity)
    t_based_on_max_a = np.sqrt((6 * abs(t1 - t0)) / max_acceleration)
    return max(t_based_on_max_v, t_based_on_max_a)


def get_coefficients_nonzero_v_and_a(t0: float, t1: float, v0: float, t_end: float, v1: float = 0) \
        -> Tuple[float, float, float, float]:
    """Retrieve trajectory formula coefficients (assuming velocity at end point is zero"""
    a_0 = t0
    a_1 = v0
    a_2 = (3 / t_end ** 2) * (t1 - t0) - (2 / t_end) * v0 - (1 / t_end) * v1
    a_3 = -(2 / t_end ** 3) * (t1 - t0) + (1 / t_end ** 2) * (v1 - v0)

    return a_0, a_1, a_2, a_3


def calculate_position(a_0: float, a_1: float, a_2: float, a_3: float, t: float) -> float:
    """Calculate position at time t"""
    return a_0 + a_1 * t + a_2 * t ** 2 + a_3 * t ** 3


def calculate_velocity(a_1: float, a_2: float, a_3: float, t: float) -> float:
    """Calculate velocity at time t"""
    return a_1 + 2 * a_2 * t + 3 * a_3 * t ** 2


def calculate_acceleration(a_2, a_3, t) -> float:
    """Calculate acceleration at time t"""
    return 2 * a_2 + 6 * a_3 * t
