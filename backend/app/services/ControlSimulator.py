from backend.app.models.ActuatorStates import ActuatorStates
from backend.app.models.RobotCrane import RobotCrane
from backend.app.services.SimpleController import SimpleController


class ControlSimulator(object):
    """Simulating the origin sensor signal and the control loop"""

    def __init__(self, robot: RobotCrane, moving_time: float):
        self.origin_sensor_frequency = 50
        self.control_frequency = 30

        self.robot = robot
        self.robot.set_act_states_t_1(self.robot.act_states_t_0) # TODO remove?

        self.moving_time = moving_time

        # Since there are no external influences, we can keep ki zero
        # Ki is set to reach the desired state quickly, but without too many oscillations
        kp, ki, kd = 0.75, 0, 0.012
        self.d1_controller = SimpleController(kp=1, ki=0, kd=0.01, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_vel)
        self.t1_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_ang_vel)
        self.t2_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_ang_vel)
        self.t3_controller = SimpleController(kp=kp, ki=ki, kd=kd, control_frequency=self.control_frequency,
                                              max_velocity=robot.max_ang_vel)

        self.time_of_last_sensor_signal = 0
        self.time_of_last_control_signal = 0

        # Initialize target end-effector position with the current robot end-effector position
        self.target_x = robot.get_x_position()
        self.target_y = robot.get_y_position()
        self.target_z = robot.get_z_position()
        self.target_phi = robot.get_phi()

        # Set initial target for controllers
        desired_act_state = self.robot.inverse_kinematics(self.target_x, self.target_y, self.target_z, self.target_phi)
        self.update_controllers_with_actuator_states(desired_act_state)

        # Initialize list for saving metrics for plotting
        self.actuator_states_list = []
        self.actual_x_positions, self.actual_y_positions, self.actual_z_positions = [], [], []
        self.target_x_positions, self.target_y_positions, self.target_z_positions = [], [], []
        self.d1_control_signals, self.t1_control_signals, self.t2_control_signals, self.t3_control_signals = [], [], [], []

    def next_step(self, t: float, next_origin: tuple) -> None | ActuatorStates:
        if t > self.moving_time:
            return None

        # Simulate origin sensor
        if self.should_simulate_origin_signal(t):
            self.time_of_last_sensor_signal = t

            if next_origin is None:
                return None

            # Update the robot origin
            self.robot.set_origin_t_1(next_origin)

            # Calculate new desired actuator states
            desired_act_state = self.robot.inverse_kinematics(self.target_x, self.target_y, self.target_z, self.target_phi)
            self.update_controllers_with_actuator_states(desired_act_state)

        # Simulate control signal with the controllers
        if self.should_simulate_control_signal(t):
            self.time_of_last_control_signal = t

            self.calculate_control_signal()

        new_act_states = self.calculate_new_actuator_states()

        self.save_metrics_for_plotting(new_act_states)
        return new_act_states

    def calculate_new_actuator_states(self) -> ActuatorStates:
        return ActuatorStates(self.robot.act_states_t_1.d_1 + self.d1_controller.signal,
                              self.robot.act_states_t_1.theta_1 + self.t1_controller.signal,
                              self.robot.act_states_t_1.theta_2 + self.t2_controller.signal,
                              self.robot.act_states_t_1.theta_3 + self.t3_controller.signal,
                              self.robot.act_states_t_1.l_6)

    def calculate_control_signal(self) -> None:
        self.d1_controller.calculate_signal(self.robot.act_states_t_1.d_1)
        self.t1_controller.calculate_signal(self.robot.act_states_t_1.theta_1)
        self.t2_controller.calculate_signal(self.robot.act_states_t_1.theta_2)
        self.t3_controller.calculate_signal(self.robot.act_states_t_1.theta_3)

    def update_controllers_with_actuator_states(self, desired_act_state: ActuatorStates) -> None:
        self.d1_controller.set_target(desired_act_state.d_1)
        self.t1_controller.set_target(desired_act_state.theta_1)
        self.t2_controller.set_target(desired_act_state.theta_2)
        self.t3_controller.set_target(desired_act_state.theta_3)

    def should_simulate_control_signal(self, t: float) -> bool:
        return t - self.time_of_last_control_signal >= (1 / self.control_frequency)

    def should_simulate_origin_signal(self, t: float) -> bool:
        return t - self.time_of_last_sensor_signal >= (1 / self.origin_sensor_frequency)

    def save_metrics_for_plotting(self, actuator_states: ActuatorStates) -> None:
        # Save actuator states
        self.actuator_states_list.append(actuator_states)

        # Save desired end-effector position
        self.target_x_positions.append(self.target_x)
        self.target_y_positions.append(self.target_y)
        self.target_z_positions.append(self.target_z)

        # Save actual end-effector position
        self.actual_x_positions.append(self.robot.get_x_position())
        self.actual_y_positions.append(self.robot.get_y_position())
        self.actual_z_positions.append(self.robot.get_z_position())

        # Save control signals
        self.d1_control_signals.append(self.d1_controller.signal)
        self.t1_control_signals.append(self.t1_controller.signal)
        self.t2_control_signals.append(self.t2_controller.signal)
        self.t3_control_signals.append(self.t3_controller.signal)
