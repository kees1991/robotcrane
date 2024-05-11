import numpy as np
from matplotlib import pyplot as plt

from Objects.ActuatorStates import ActuatorStates
from Objects.RobotCrane import RobotCrane
from Objects.SimpleController import SimpleController

if __name__ == '__main__':
    robot = RobotCrane()

    # time-series
    duration = 100
    time_step_size = 0.1
    time_list = np.linspace(0, duration, int(np.ceil(duration / time_step_size)))

    # move robot
    x = 0.3
    y = 0.4
    z = 0.2
    phi = np.deg2rad(90)
    act_states = robot.inverse_kinematics(x, y, z, phi)
    robot.set_act_states_t_1(act_states)

    # commands
    commands = [[0, 0.3, y, 0.4], [4, 0.3, y, 0.5], [20, 0.4, y, 0.4], [40, 0.5, y, 0.3], [60, 0.6, y, 0.2], [80, 0.7, y, 0.5]]
    # commands = [[0, x, y, 0.2], [1, x, y, 0.8]]

    command_idx = 0
    new_x_target = commands[0][1]
    x_target_list = [new_x_target]

    new_z_target = commands[0][3]
    z_target_list = [new_z_target]

    # init position lists
    x = [robot.get_x_position()]
    z = [robot.get_z_position()]

    # Init controllers
    sample_rate = 2
    kp, ki, kd = 0.35, 0, 0.019
    time_step_index_for_updating_signal = round(sample_rate/time_step_size)
    d1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=1)
    t1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=1)
    t2_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=1)
    t3_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=1)

    for i in range(1, len(time_list)):

        if command_idx <= len(commands) - 1:
            if commands[command_idx][0] <= round(time_list[i], 2):
                new_x_target = commands[command_idx][1]
                new_z_target = commands[command_idx][3]
                command_idx += 1

                desired_act_state = robot.inverse_kinematics(new_x_target, y, new_z_target, phi)

                d1_controller.set_target(desired_act_state.d_1)
                t1_controller.set_target(desired_act_state.theta_1)
                t2_controller.set_target(desired_act_state.theta_2)
                t3_controller.set_target(desired_act_state.theta_3)

        x_target_list.append(new_x_target)
        z_target_list.append(new_z_target)

        if i % time_step_index_for_updating_signal == 0:
            d1_controller.adjust_signal(robot.act_states_t_1.d_1)
            t1_controller.adjust_signal(robot.act_states_t_1.theta_1)
            t2_controller.adjust_signal(robot.act_states_t_1.theta_2)
            t3_controller.adjust_signal(robot.act_states_t_1.theta_3)
        else:
            d1_controller.update_signal_list()
            t1_controller.update_signal_list()
            t2_controller.update_signal_list()
            t3_controller.update_signal_list()


        robot.set_act_states_t_1(
            ActuatorStates(robot.act_states_t_1.d_1 + d1_controller.signal,
                           robot.act_states_t_1.theta_1 + t1_controller.signal,
                           robot.act_states_t_1.theta_2 + t2_controller.signal,
                           robot.act_states_t_1.theta_3 + t3_controller.signal,
                           robot.act_states_t_1.l_6))

        x.append(robot.get_x_position())
        z.append(robot.get_z_position())

    fig_z, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, constrained_layout=True)

    ax1.plot(time_list, z_target_list, color='#7c8994', label='Target')
    ax1.plot(time_list, z, color='#296ca3', alpha=0.7, label='Position')
    ax1.legend()
    ax1.set_ylabel('Z-position')
    ax1.set_title('Target and Z-position')

    print("Total error for D1: {}".format(d1_controller.total_error))

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

    fig_x, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, constrained_layout=True)

    ax1.plot(time_list, x_target_list, color='#7c8994', label='Target')
    ax1.plot(time_list, x, color='#296ca3', alpha=0.7, label='Position')
    ax1.legend()
    ax1.set_ylabel('X-position')
    ax1.set_title('Target and X-position')

    print("Total error for Theta1: {}".format(t1_controller.total_error))
    print("Total error for Theta2: {}".format(t2_controller.total_error))
    print("Total error for Theta3: {}".format(t3_controller.total_error))

    ax2.plot(time_list, t1_controller.signal_list, color='#7c8994', label='Theta 1')
    ax2.plot(time_list, t2_controller.signal_list, color='#296ca3', label='Theta 2')
    ax2.plot(time_list, t3_controller.signal_list, color='#296ca3', label='Theta 3')
    ax2.legend()
    ax2.set_ylabel('Signal')
    ax2.set_title('Theta Signal over time')

    x_error = []
    for i in range(0, len(x_target_list)):
        x_error.append(x_target_list[i]-x[i])

    ax3.plot(time_list, x_error, color='#7c8994', label='X-error')
    ax3.legend()
    ax3.set_ylabel('X-error')
    ax3.set_title('X-error over time')

    plt.show()
