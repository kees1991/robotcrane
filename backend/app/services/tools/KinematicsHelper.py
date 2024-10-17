import numpy as np
from math import sin as s, cos as c
from numpy.linalg import inv


def calculate_dh_parameters(l_21, l_31, d_41, l_51, act_states_t_1):
    l_2, l_3, d_4, l_5 = l_21, l_31, d_41, l_51
    d_1, theta_1, theta_2, theta_3, l_6 = act_states_t_1.get_states()
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


def calculate_transformation_matrices(dh, num_axis, t_origin):
    """Calculate transformation matrices for each joint and origin"""
    t_matrices = np.zeros((num_axis + 1, 4, 4))
    t_matrices[0] = inv(t_origin)

    for axis in range(num_axis):
        t_matrices[axis + 1] = trans_matrix_from_dh(dh[axis])

    return t_matrices


def calculate_state_frames(size, t_matrices):
    """Calculate the robot state frames with the transformation matrices"""
    fs = np.zeros((7, 4, 4))
    frame = np.eye(4)
    for i in range(size + 1):
        frame = np.dot(frame, t_matrices[i])
        fs[i] = frame
    return fs


def calculate_origin_translation_matrix(new_origin):
    x, y, z, phi = new_origin[0], new_origin[1], new_origin[2], new_origin[3]
    return np.array(
        [
            [np.cos(phi), np.sin(phi), 0., -x],
            [-np.sin(phi), np.cos(phi), 0., -y],
            [0., 0., 1., -z],
            [0., 0., 0., 1.]
        ]
    )
