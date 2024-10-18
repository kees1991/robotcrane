from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.models.OriginTrajectory import OriginTrajectory
from backend.app.services.SimpleController import SimpleController


class ControlSimulator(object):
    """Simulating the origin sensor signal and the control loop"""

    def __init__(self, robot):
        self.origin_sensor_frequency = 20
        self.time_of_last_sensor_signal = 0
        self.control_frequency = 20
        self.time_of_last_control_signal = 0

        self.robot = robot
        self.robot.set_act_states_t_1(self.robot.act_states_t_0)

        self.new_org = self.robot.origin_t_1
        self.robot.set_origin_t_1(self.robot.origin_t_0)

        self.org_traj = OriginTrajectory(robot.origin_t_0, self.new_org)
        self.duration = self.org_traj.mov_time
        print(f"Moving time: {self.org_traj.mov_time}")

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
        self.x, self.y, self.z = [robot.get_x_position()], [robot.get_y_position()], [robot.get_z_position()]
        self.x_targets, self.y_targets, self.z_targets = [self.x_d], [self.y_d], [self.z_d]

        desired_act_state = self.robot.inverse_kinematics(self.x_d, self.y_d, self.z_d, self.phi_d)
        self.d1_controller.set_target(desired_act_state.d_1)
        self.t1_controller.set_target(desired_act_state.theta_1)
        self.t2_controller.set_target(desired_act_state.theta_2)
        self.t3_controller.set_target(desired_act_state.theta_3)

    def origin_next_step(self, t):
        return self.org_traj.origin_next_step(t)

    def next_step(self, t):
        if t > self.duration:
            return None

        # Simulate origin sensor
        if t - self.time_of_last_sensor_signal >= (1/self.origin_sensor_frequency):
            self.time_of_last_sensor_signal = t

            next_origin = self.org_traj.origin_next_step(t)
            if next_origin is None:
                return None

            self.robot.set_origin_t_1(tuple(next_origin))

            desired_act_state = self.robot.inverse_kinematics(self.x_d, self.y_d, self.z_d, self.phi_d)

            self.d1_controller.set_target(desired_act_state.d_1)
            self.t1_controller.set_target(desired_act_state.theta_1)
            self.t2_controller.set_target(desired_act_state.theta_2)
            self.t3_controller.set_target(desired_act_state.theta_3)

        # Simulate control signal
        if t - self.time_of_last_control_signal >= (1/self.control_frequency):
            self.time_of_last_control_signal = t

            self.d1_controller.calculate_signal(self.robot.act_states_t_1.d_1)
            self.t1_controller.calculate_signal(self.robot.act_states_t_1.theta_1)
            self.t2_controller.calculate_signal(self.robot.act_states_t_1.theta_2)
            self.t3_controller.calculate_signal(self.robot.act_states_t_1.theta_3)
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
