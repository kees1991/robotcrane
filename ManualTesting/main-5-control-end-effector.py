import numpy as np

from Objects.ActuatorStates import ActuatorStates
from Objects.RobotCrane import RobotCrane
from Objects.SimpleController import SimpleController
from Tooling.plotting import plot_control_metrics

if __name__ == '__main__':
    """Test control loop"""
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
    commands = [[0, 0.3, y, 0.2], [4, 0.3, y, 0.3], [20, 0.4, y, 0.4], [40, 0.5, y, 0.3], [60, 0.6, y, 0.2], [80, 0.7, y, 0.5]]

    command_idx = 0
    new_x_target = commands[0][1]
    x_target_list = [new_x_target]

    new_y_target = y
    y_target_list = [y]

    new_z_target = commands[0][3]
    z_target_list = [new_z_target]

    # init position lists
    x = [robot.get_x_position()]
    y = [robot.get_y_position()]
    z = [robot.get_z_position()]

    # Init controllers
    sample_rate = 1
    kp, ki, kd = 0.15, 0, 0.019
    time_step_index_for_updating_signal = round(sample_rate/time_step_size)
    d1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=0.1)
    t1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=0.5)
    t2_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=0.5)
    t3_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=sample_rate, max_velocity=0.5)

    for i in range(1, len(time_list)):

        if command_idx <= len(commands) - 1:
            if commands[command_idx][0] <= round(time_list[i], 2):
                new_x_target = commands[command_idx][1]
                new_z_target = commands[command_idx][3]
                command_idx += 1

                desired_act_state = robot.inverse_kinematics(new_x_target, new_y_target, new_z_target, phi)

                d1_controller.set_target(desired_act_state.d_1)
                t1_controller.set_target(desired_act_state.theta_1)
                t2_controller.set_target(desired_act_state.theta_2)
                t3_controller.set_target(desired_act_state.theta_3)

        x_target_list.append(new_x_target)
        y_target_list.append(new_y_target)
        z_target_list.append(new_z_target)

        if i % time_step_index_for_updating_signal == 0:
            d1_controller.calculate_signal(robot.act_states_t_1.d_1)
            t1_controller.calculate_signal(robot.act_states_t_1.theta_1)
            t2_controller.calculate_signal(robot.act_states_t_1.theta_2)
            t3_controller.calculate_signal(robot.act_states_t_1.theta_3)
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
        y.append(robot.get_y_position())
        z.append(robot.get_z_position())

    plot_control_metrics(time_list, x, y, z, x_target_list, y_target_list, z_target_list,
                         d1_controller, t1_controller, t2_controller, t3_controller)
