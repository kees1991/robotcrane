import numpy as np
from matplotlib import pyplot as plt


def plot_robot(robot):
    frames = robot.get_frames()

    plot_xlim, plot_ylim, plot_zlim = [-1, 1], [-1, 1], [0.0, 1.0]
    figure = plt.figure()
    ax = figure.add_subplot(111, projection="3d")
    ax.set_xlim(plot_xlim)
    ax.set_ylim(plot_ylim)
    ax.set_zlim(plot_zlim)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    x, y, z = [0.], [0.], [0.]
    axis_frames = frames
    for i in range(len(frames)):
        x.append(axis_frames[i][0:3, 3:4][0, 0])
        y.append(axis_frames[i][0:3, 3:4][1, 0])
        z.append(axis_frames[i][0:3, 3:4][2, 0])
    ax.plot_wireframe(x, y, np.array([z]))
    ax.scatter(x[1:], y[1:], z[1:], c="red", marker="o")
    # plot axes using cylinders
    params = robot.dh_params[:, 0:3]
    cy_radius = np.amax(params[:, 0:2]) * 0.05
    cy_len = cy_radius * 4.
    cy_div = 4 + 1
    theta = np.linspace(0, 2 * np.pi, cy_div)
    cx = np.array([cy_radius * np.cos(theta)])
    cz = np.array([-0.5 * cy_len, 0.5 * cy_len])
    cx, cz = np.meshgrid(cx, cz)
    cy = np.array([cy_radius * np.sin(theta)] * 2)
    points = np.zeros([3, cy_div * 2])
    points[0] = cx.flatten()
    points[1] = cy.flatten()
    points[2] = cz.flatten()
    ax.plot_surface(points[0].reshape(2, cy_div), points[1].reshape(2, cy_div), points[2].reshape(2, cy_div),
                    color="pink", rstride=1, cstride=1, linewidth=0, alpha=0.4)
    for i in range(len(frames) - 1):
        f = axis_frames[i]
        points_f = f[0:3, 0:3].dot(points) + f[0:3, 3:4]
        ax.plot_surface(points_f[0].reshape(2, cy_div), points_f[1].reshape(2, cy_div),
                        points_f[2].reshape(2, cy_div)
                        , color="pink", rstride=1, cstride=1, linewidth=0, alpha=0.4)
    # plot the end frame
    f = axis_frames[-1]
    ax.plot_wireframe(np.array([f[0, 3], f[0, 3] + 0.2 * f[0, 0]]),
                      np.array([f[1, 3], f[1, 3] + 0.2 * f[1, 0]]),
                      np.array([[f[2, 3], f[2, 3] + 0.2 * f[2, 0]]]), color="red")
    ax.plot_wireframe(np.array([f[0, 3], f[0, 3] + 0.2 * f[0, 1]]),
                      np.array([f[1, 3], f[1, 3] + 0.2 * f[1, 1]]),
                      np.array([[f[2, 3], f[2, 3] + 0.2 * f[2, 1]]]), color="green")
    ax.plot_wireframe(np.array([f[0, 3], f[0, 3] + 0.2 * f[0, 2]]),
                      np.array([f[1, 3], f[1, 3] + 0.2 * f[1, 2]]),
                      np.array([[f[2, 3], f[2, 3] + 0.2 * f[2, 2]]]), color="blue")


def plot_trajectory(act_states):
    ts = []

    d1, t1, t2, t3, l6 = [], [], [], [], []
    d1_v, t1_v, t2_v, t3_v, l6_v = [], [], [], [], []
    d1_a, t1_a, t2_a, t3_a, l6_a = [], [], [], [], []

    counter = 0
    for act_state in act_states:
        ts.append(counter)

        d1.append(act_state.d_1)
        t1.append(act_state.theta_1)
        t2.append(act_state.theta_2)
        t3.append(act_state.theta_3)
        l6.append(act_state.l_6)

        d1_v.append(act_state.d_1_v)
        t1_v.append(act_state.theta_1_v)
        t2_v.append(act_state.theta_2_v)
        t3_v.append(act_state.theta_3_v)
        l6_v.append(act_state.l_6_v)

        d1_a.append(act_state.d_1_a)
        t1_a.append(act_state.theta_1_a)
        t2_a.append(act_state.theta_2_a)
        t3_a.append(act_state.theta_3_a)
        l6_a.append(act_state.l_6_a)

        counter += 1

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, constrained_layout=True)
    ax1.plot(ts, d1, color='#F1C40F', label='D1')
    ax1.plot(ts, t1, color='#0914e6', label='Theta 1')
    ax1.plot(ts, t2, color='#e31425', label='Theta 2')
    ax1.plot(ts, t3, color='#e3dc09', label='Theta 3')
    ax1.plot(ts, l6, color='#E74C3C', label='L6')
    ax1.legend()
    ax1.set_ylabel('Position')
    ax1.set_title('Theta 1,2,3 Position')

    ax2.plot(ts, d1_v, color='#F1C40F', label='D1')
    ax2.plot(ts, t1_v, color='#0914e6', label='Theta 1')
    ax2.plot(ts, t2_v, color='#e31425', label='Theta 2')
    ax2.plot(ts, t3_v, color='#e3dc09', label='Theta 3')
    ax2.plot(ts, l6_v, color='#E74C3C', label='L6')
    ax2.legend()
    ax2.set_ylabel('Velocity')
    ax2.set_title('Theta 1,2,3 Velocity')

    ax3.plot(ts, d1_a, color='#F1C40F', label='D1')
    ax3.plot(ts, t1_a, color='#0914e6', label='Theta 1')
    ax3.plot(ts, t2_a, color='#e31425', label='Theta 2')
    ax3.plot(ts, t3_a, color='#e3dc09', label='Theta 3')
    ax3.plot(ts, l6_a, color='#E74C3C', label='L6')
    ax3.legend()
    ax3.set_ylabel('Acceleration')
    ax3.set_title('Theta 1,2,3 Acceleration')


def plot_org_trajectory(org_time_series):
    ts = []
    org_x = []
    org_y = []
    org_z = []
    org_phi = []

    counter = 0
    for org in org_time_series:
        ts.append(counter)
        org_x.append(org[0])
        org_y.append(org[1])
        org_z.append(org[2])
        org_phi.append(org[3])

        counter += 1

    fig, (ax1) = plt.subplots(1, sharex=True, constrained_layout=True)
    ax1.plot(ts, org_x, color='#0914e6', label='Org x')
    ax1.plot(ts, org_y, color='#e31425', label='Org y')
    ax1.plot(ts, org_z, color='#e3dc09', label='Org z')
    ax1.legend()
    ax1.set_ylabel('Org position')
    ax1.set_title('Org position')


def plot_control_metrics(time_list, x, y, z, x_target_list, y_target_list, z_target_list, d1_controller, t1_controller,
                         t2_controller, t3_controller):
    # Plot Z-error
    fig_z, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, constrained_layout=True)

    ax1.plot(time_list, z_target_list, color='#7c8994', label='Target')
    ax1.plot(time_list, z, color='#296ca3', alpha=0.7, label='Position')
    ax1.legend()
    ax1.set_ylabel('Z-position')
    ax1.set_title('Target and Z-position')

    print(f"Total error for D1: {d1_controller.total_error}")

    ax2.plot(time_list, d1_controller.signal_list, color='#7c8994', label='D1 signal')
    ax2.plot(time_list, d1_controller.uncapped_signal_list, color='#7c8994', label='D1 uncapped signal')
    ax2.legend()
    ax2.set_ylabel('Signal')
    ax2.set_title('D1 Signal over time')

    z_error = []
    for i in range(0, len(x_target_list)):
        z_error.append(z_target_list[i] - z[i])

    ax3.plot(time_list, z_error, color='#7c8994', label='Z-error')
    ax3.legend()
    ax3.set_ylabel('Z-error')
    ax3.set_title('Z-error over time')

    # Plot X,Y-error
    fig_x, (ax_x, ax_y, ax_xt, ax_xe, ax_ye) = plt.subplots(5, sharex=True, constrained_layout=True)

    ax_x.plot(time_list, x_target_list, color='#7c8994', label='Target')
    ax_x.plot(time_list, x, color='#296ca3', alpha=0.7, label='Position')
    ax_x.legend()
    ax_x.set_ylabel('X-position')
    ax_x.set_title('Target and X-position')

    ax_y.plot(time_list, y_target_list, color='#7c8994', label='Target')
    ax_y.plot(time_list, y, color='#296ca3', alpha=0.7, label='Position')
    ax_y.legend()
    ax_y.set_ylabel('Y-position')
    ax_y.set_title('Target and Y-position')

    print(f"Total error for Theta1: {t1_controller.total_error}")
    print(f"Total error for Theta2: {t2_controller.total_error}")
    print(f"Total error for Theta3: {t3_controller.total_error}")

    ax_xt.plot(time_list, t1_controller.signal_list, color='#7c8994', label='Theta 1')
    ax_xt.plot(time_list, t2_controller.signal_list, color='#296ca3', label='Theta 2')
    ax_xt.plot(time_list, t3_controller.signal_list, color='#296ca3', label='Theta 3')
    ax_xt.legend()
    ax_xt.set_ylabel('Signal')
    ax_xt.set_title('Theta signal over time')

    x_error = []
    for i in range(0, len(x_target_list)):
        x_error.append(x_target_list[i] - x[i])

    ax_xe.plot(time_list, x_error, color='#7c8994', label='X-error')
    ax_xe.legend()
    ax_xe.set_ylabel('X-error')
    ax_xe.set_title('X-error over time')

    y_error = []
    for i in range(0, len(y_target_list)):
        y_error.append(y_target_list[i] - y[i])

    ax_ye.plot(time_list, y_error, color='#7c8994', label='Y-error')
    ax_ye.legend()
    ax_ye.set_ylabel('Y-error')
    ax_ye.set_title('Y-error over time')

    plt.show()
