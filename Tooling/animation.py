import datetime

from matplotlib import pyplot as plt, animation


def setup_animation_axes_3d():
    fig = plt.figure(figsize=(16, 9), dpi=80)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, 3)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    joint_lines = [ax.plot([], [], [], 'o-', linewidth=2, markersize=4)[0] for _ in range(7)]
    trajectory_line, = ax.plot([], [], [], 'r--', linewidth=1.5)

    return fig, ax, joint_lines, trajectory_line


def convert_to_xyz_tuple(frame):
    frame_t = frame[0:3, 3:4].T
    return tuple(map(tuple, frame_t))[0]


def animate_3d(frame, act_states_time_series, robotcrane, joint_lines, trajectory_line):
    end_effector_positions = []

    for i in range(frame):
        act_states = act_states_time_series[i]
        robotcrane.set_act_states_t_1(act_states)
        frames = robotcrane.get_frames()

        # slice frame to x,y,z
        end_frame = frames[-1]

        end_effector_positions.append(convert_to_xyz_tuple(end_frame))

        for j in range(len(joint_lines)):
            xs, ys, zs = zip(
                *[convert_to_xyz_tuple(frames[j - 1]), convert_to_xyz_tuple(frames[j])] if j > 0
                else [(0, 0, 0), convert_to_xyz_tuple(frames[j])]
            )
            joint_lines[j].set_data(xs, ys)
            joint_lines[j].set_3d_properties(zs)

    if end_effector_positions:
        trajectory_x, trajectory_y, trajectory_z = zip(*end_effector_positions)
        trajectory_line.set_data(trajectory_x, trajectory_y)
        trajectory_line.set_3d_properties(trajectory_z)

    return joint_lines + [trajectory_line]


def animate_3d_with_origin(frame, act_states_time_series, org_time_series, robotcrane, joint_lines, trajectory_line):
    end_effector_positions = []

    for i in range(frame):
        act_states = act_states_time_series[i]
        robotcrane.set_act_states_t_1(act_states)
        robotcrane.set_new_origin(tuple(org_time_series[i]))
        frames = robotcrane.get_frames()

        # slice frame to x,y,z
        end_frame = frames[-1]

        end_effector_positions.append(convert_to_xyz_tuple(end_frame))

        for j in range(len(joint_lines)):
            xs, ys, zs = zip(
                *[convert_to_xyz_tuple(frames[j - 1]), convert_to_xyz_tuple(frames[j])] if j > 0
                else [(0, 0, 0), convert_to_xyz_tuple(frames[j])]
            )
            joint_lines[j].set_data(xs, ys)
            joint_lines[j].set_3d_properties(zs)

    if end_effector_positions:
        trajectory_x, trajectory_y, trajectory_z = zip(*end_effector_positions)
        trajectory_line.set_data(trajectory_x, trajectory_y)
        trajectory_line.set_3d_properties(trajectory_z)

    return joint_lines + [trajectory_line]


def create_control_animation(act_states_list, org_time_series, robot):
    fig, ax, joint_lines, trajectory_line = setup_animation_axes_3d()
    ani = animation.FuncAnimation(fig, animate_3d_with_origin, len(act_states_list),
                                  fargs=(
                                      act_states_list, org_time_series, robot, joint_lines, trajectory_line),
                                  interval=25, blit=True)

    ct = datetime.datetime.now()
    ani.save(f"robot-crane-control-{ct.timestamp()}.mp4", fps=30, extra_args=['-vcodec', 'libx264'])
