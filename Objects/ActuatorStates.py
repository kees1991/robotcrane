class ActuatorStates(object):
    """Define the actuator states of the robot"""

    def __init__(self,
                 d_1, theta_1, theta_2, theta_3, l_6,
                 d_1_v=0, theta_1_v=0, theta_2_v=0, theta_3_v=0, l_6_v=0,
                 d_1_a=0, theta_1_a=0, theta_2_a=0, theta_3_a=0, l_6_a=0):
        """Initialise Actuator position, velocity and acceleration"""
        self.d_1 = d_1          # lift in mm
        self.theta_1 = theta_1  # swing in degrees
        self.theta_2 = theta_2  # elbow rotation in degrees
        self.theta_3 = theta_3  # wrist rotation in degrees
        self.l_6 = l_6          # jaw opening in mm

        self.d_1_v, self.theta_1_v, self.theta_2_v, self.theta_3_v, self.l_6_v = d_1_v, theta_1_v, theta_2_v, theta_3_v, l_6_v
        self.d_1_a, self.theta_1_a, self.theta_2_a, self.theta_3_a, self.l_6_a = d_1_a, theta_1_a, theta_2_a, theta_3_a, l_6_a

    def get_states(self):
        return self.d_1, self.theta_1, self.theta_2, self.theta_3, self.l_6

    def reset_vel_and_acc(self):
        self.d_1_v, self.theta_1_v, self.theta_2_v, self.theta_3_v, self.l_6_v = 0, 0, 0, 0, 0
        self.d_1_a, self.theta_1_a, self.theta_2_a, self.theta_3_a, self.l_6_a = 0, 0, 0, 0, 0

    def __str__(self):
        return ((
            f"d1 = {self.d_1}, theta1 = {self.theta_1}, theta2 = {self.theta_2}, theta3 = {self.theta_3}, l_6 = {self.l_6}\n"
            f"d1 v = {self.d_1_v}, theta1 v = {self.theta_1_v}, theta2 v = {self.theta_2_v}, theta3 v = {self.theta_3_v}, l_6 v = {self.l_6_v}\n"
            f"d1 a = {self.d_1_a}, theta1 a = {self.theta_1_a}, theta2 a = {self.theta_2_a}, theta3 a = {self.theta_3_a}, l_6 a = {self.l_6_a}")
        )
