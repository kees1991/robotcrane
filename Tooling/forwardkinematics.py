import numpy as np
from math import sin as s, cos as c
from numpy.linalg import inv


def calculate_dh_params(l_2, l_3, d_4, l_5, d_1, theta_1, theta_2, theta_3, l_6):
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


def trans_matrix_from_dh(dh_params):
    d, a, alpha, theta = dh_params
    return np.array(
        [
            [c(theta), -s(theta) * c(alpha), s(theta) * s(alpha), a * c(theta)],
            [s(theta), c(theta) * c(alpha), -c(theta) * s(alpha), a * s(theta)],
            [0., s(alpha), c(alpha), d],
            [0., 0., 0., 1.]
        ]
    )


def retrieve_ts(dh, num_axis, t_origin):
    t_matrices = np.zeros((num_axis + 1, 4, 4))
    t_matrices[0] = inv(t_origin)

    for axis in range(num_axis):
        t_matrices[axis + 1] = trans_matrix_from_dh(dh[axis])

    return t_matrices


def retrieve_frames(size, t_matrices):
    fs = np.zeros((7, 4, 4))
    frame = np.eye(4)
    for i in range(size + 1):
        frame = np.dot(frame, t_matrices[i])
        fs[i] = frame
    return fs
