import numpy as np
from math import sin as s, cos as c
from numpy.linalg import inv


def trans_matrix_from_dh(dh_params):
    """Calculate transformation matrix based on the DH parameters"""
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
    """Calculate transformation matrices for each joint and origin"""
    t_matrices = np.zeros((num_axis + 1, 4, 4))
    t_matrices[0] = inv(t_origin)

    for axis in range(num_axis):
        t_matrices[axis + 1] = trans_matrix_from_dh(dh[axis])

    return t_matrices


def retrieve_frames(size, t_matrices):
    """Retrieve the robot state frames with the transformation matrices"""
    fs = np.zeros((7, 4, 4))
    frame = np.eye(4)
    for i in range(size + 1):
        frame = np.dot(frame, t_matrices[i])
        fs[i] = frame
    return fs
