import numpy as np

from Objects.ActuatorStates import ActuatorStates
from Objects.OriginTrajectory import OriginTrajectory
from Objects.SimpleController import SimpleController
from Tooling.plot_tools import plot_control_metrics


class ControlSimulator(object):
    def __init__(self, robot):
        self.origin_sensor_frequency = 20  # Hz
        self.time_of_last_sensor_signal = 0

        self.control_frequency = 20  # Hz
        self.time_of_last_control_signal = 0

        self.robot = robot
        self.robot.set_act_states_t_1(self.robot.act_states_t_0)

        self.new_org = self.robot.origin_t_1
        self.robot.set_new_origin(self.robot.origin_t_0)

        self.org_traj = OriginTrajectory(robot.origin_t_0, self.new_org)
        self.duration = self.org_traj.mov_time
        print("Moving time: {}".format(self.org_traj.mov_time))

        kp, ki, kd = 0.3, 0.74, 0.001
        self.d1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_vel)
        self.t1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_ang_vel)
        self.t2_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_ang_vel)
        self.t3_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_ang_vel)

        # Init end-effector desired position
        self.x_d = robot.get_x_position()
        self.y_d = robot.get_y_position()
        self.z_d = robot.get_z_position()
        self.phi_d = robot.get_phi()

        # Init lists
        self.act_states_list = []
        self.x = [robot.get_x_position()]
        self.x_targets = [self.x_d]
        self.y = [robot.get_y_position()]
        self.y_targets = [self.y_d]
        self.z = [robot.get_z_position()]
        self.z_targets = [self.z_d]

        desired_act_state = self.robot.inverse_kinematics(self.x_d, self.y_d, self.z_d, self.phi_d)
        self.d1_controller.set_target(desired_act_state.d_1)
        self.t1_controller.set_target(desired_act_state.theta_1)
        self.t2_controller.set_target(desired_act_state.theta_2)
        self.t3_controller.set_target(desired_act_state.theta_3)

    def origin_next_step_real_time(self, t):
        return self.org_traj.origin_next_step_real_time(t)

    def trajectory_next_step_real_time(self, t):
        if t > self.duration:
            return None

        # Simulate origin sensor
        if t - self.time_of_last_sensor_signal >= (1/self.origin_sensor_frequency):
            self.time_of_last_sensor_signal = t

            next_origin = self.org_traj.origin_next_step_real_time(t)
            if next_origin is None:
                return None

            self.robot.set_new_origin(tuple(next_origin))

            desired_act_state = self.robot.inverse_kinematics(self.x_d, self.y_d, self.z_d, self.phi_d)

            self.d1_controller.set_target(desired_act_state.d_1)
            self.t1_controller.set_target(desired_act_state.theta_1)
            self.t2_controller.set_target(desired_act_state.theta_2)
            self.t3_controller.set_target(desired_act_state.theta_3)

        # Simulate control signal
        if t - self.time_of_last_control_signal >= (1/self.control_frequency):
            self.time_of_last_control_signal = t

            self.d1_controller.adjust_signal(self.robot.act_states_t_1.d_1)
            self.t1_controller.adjust_signal(self.robot.act_states_t_1.theta_1)
            self.t2_controller.adjust_signal(self.robot.act_states_t_1.theta_2)
            self.t3_controller.adjust_signal(self.robot.act_states_t_1.theta_3)
        else:
            self.d1_controller.update_signal_list()
            self.t1_controller.update_signal_list()
            self.t2_controller.update_signal_list()
            self.t3_controller.update_signal_list()

        new_act_states = ActuatorStates(self.robot.act_states_t_1.d_1 + self.d1_controller.signal,
                                        self.robot.act_states_t_1.theta_1 + self.t1_controller.signal,
                                        self.robot.act_states_t_1.theta_2 + self.t2_controller.signal,
                                        self.robot.act_states_t_1.theta_3 + self.t3_controller.signal,
                                        self.robot.act_states_t_1.l_6)

        self.robot.set_act_states_t_1(new_act_states)
        self.act_states_list.append(new_act_states)

        self.add_metrics_for_plotting(self.robot, self.x_d, self.y_d, self.z_d)
        return new_act_states

    def add_metrics_for_plotting(self, robot, x_d, y_d, z_d):
        self.x_targets.append(x_d)
        self.y_targets.append(y_d)
        self.z_targets.append(z_d)
        self.x.append(robot.get_x_position())
        self.y.append(robot.get_y_position())
        self.z.append(robot.get_z_position())

    def plot_metrics(self, time_list):
        plot_control_metrics(time_list, self.x, self.y, self.z, self.x_targets, self.y_targets, self.z_targets,
                             self.d1_controller, self.t1_controller, self.t2_controller, self.t3_controller)
