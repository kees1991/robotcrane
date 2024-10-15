class SimpleController(object):
    """Controller to create a control signal for the robot"""

    def __init__(self, kp=1, ki=0, kd=0, control_frequency=20, max_velocity=1):
        self.max_signal = max_velocity/control_frequency
        self.sample_rate = 1/control_frequency
        self.kp = kp
        self.kd = kd
        self.ki = ki

        self.error_sum = 0
        self.last_reading = None

        self.target = None
        self.signal = 0

        self.total_error = 0
        self.uncapped_signal_list = [0]
        self.signal_list = [0]

    def set_target(self, target):
        self.error_sum = 0
        self.target = target

    def calculate_signal(self, actual_value):
        error = self.target - actual_value

        if self.last_reading is None:
            self.last_reading = actual_value

        self.error_sum += error

        # Calculate controller signal
        self.signal = self.kp * error + self.ki * self.error_sum + self.kd * (
                    actual_value - self.last_reading) / self.sample_rate

        self.uncapped_signal_list.append(self.signal)

        # Cap signal based on max velocity
        if self.signal > self.max_signal:
            self.signal = self.max_signal
        elif self.signal < -self.max_signal:
            self.signal = -self.max_signal

        self.signal_list.append(self.signal)
        self.total_error += abs(error)

        # Store last value
        self.last_reading = actual_value

    def update_signal_list(self):
        self.uncapped_signal_list.append(self.signal)
        self.signal_list.append(self.signal)
