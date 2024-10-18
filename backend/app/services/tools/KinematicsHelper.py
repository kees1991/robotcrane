import numpy as np
from math import sin as s, cos as c
from numpy.linalg import inv


def calculate_dh_parameters(l_2, l_3, d_4, l_5, act_states_t_1):
    """Calculate the Denavit-Hartenberg parameters based on the robot dimensions and the actuator states"""
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


def calculate_transformation_matrices(dh, t_origin):
    """Calculate transformation matrices for each joint and origin"""
    axis_count = len(dh)

    t_matrices = np.zeros((axis_count + 1, 4, 4))
    t_matrices[0] = inv(t_origin)

    for axis in range(axis_count):
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


def calculate_origin_translation_matrix(origin):
    """Calculate the translation matrix for an origin"""
    x, y, z, phi = origin[0], origin[1], origin[2], origin[3]
    return np.array(
        [
            [np.cos(phi), np.sin(phi), 0., -x],
            [-np.sin(phi), np.cos(phi), 0., -y],
            [0., 0., 1., -z],
            [0., 0., 0., 1.]
        ]
    )


def translate_desired_end_effector_state_for_new_origin(T_origin, origin_t_1, phi, x, y, z):
    """Calculate an end-effector desired state wrt to a new origin"""
    translated_goal = np.dot(T_origin, np.array([x, y, z, 1]))
    x, y, z = translated_goal[0], translated_goal[1], translated_goal[2]
    if origin_t_1 is not None:
        phi -= origin_t_1[3]
    return phi, x, y, z


def calculate_inverse_kinematics(l_2, l_3, d_4, l_5, do_open_gripper, phi, x, y, z):
    l_6 = calculate_jaw_opening(do_open_gripper)

    g_x, g_y = calculate_gripper_position(l_6, phi, x, y)
    w_x, w_y = calculate_wrist_position(l_5, phi, g_x, g_y)

    theta_2 = calculate_elbow_rotation(l_2, l_3, w_x, w_y)
    theta_1 = calculate_swing_rotation(l_2, l_3, theta_2, w_x, w_y)
    theta_3 = calculate_wrist_rotation(phi, theta_1, theta_2)

    d_1 = calculate_lift_position(d_4, z)

    return d_1, theta_1, theta_2, theta_3, l_6


def calculate_jaw_opening(do_open_gripper):
    # For inverse kinematics we assume that gripper will be open or closed
    if do_open_gripper:
        return 0.1
    else:
        return 0.0


def calculate_gripper_position(l_6, phi, x, y):
    g_x = x - l_6 * np.cos(phi)
    g_y = y - l_6 * np.sin(phi)
    return g_x, g_y


def calculate_elbow_rotation(l_2, l_3, w_x, w_y):
    c_2 = (w_x ** 2 + w_y ** 2 - l_2 ** 2 - l_3 ** 2) / (2 * l_2 * l_3)

    if c_2 > 1:
        print(f"Cos of theta 2 is {c_2}, while it cannot be larger than 1")
        raise ValueError("Given end-effector position is out of reach")

    # Other solution: - np.sqrt(1 - c_2 ** 2)
    s_2 = np.sqrt(1 - c_2 ** 2)
    return np.arctan2(s_2, c_2)


def calculate_swing_rotation(l_2, l_3, theta_2, w_x, w_y):
    k_1 = l_2 + l_3 * (np.cos(theta_2))
    k_2 = l_3 * (np.sin(theta_2))
    return np.arctan2(w_y, w_x) - np.arctan2(k_2, k_1)


def calculate_wrist_rotation(phi, theta_1, theta_2):
    return phi - theta_1 - theta_2


def calculate_wrist_position(l_5, phi, g_x, g_y):
    w_x = g_x - l_5 * np.cos(phi)
    w_y = g_y - l_5 * np.sin(phi)
    return w_x, w_y


def calculate_lift_position(d_4, z):
    return z - d_4
