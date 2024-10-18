from typing import Tuple


class ActuatorStates(object):
    """Define the actuator states of the robot"""
    def __init__(self,
                 d_1: float, theta_1: float, theta_2: float, theta_3: float, l_6: float,
                 d_1_v: float = 0.0, theta_1_v: float = 0.0, theta_2_v: float = 0.0, theta_3_v: float = 0.0,
                 l_6_v: float = 0.0,
                 d_1_a: float = 0.0, theta_1_a: float = 0.0, theta_2_a: float = 0.0, theta_3_a: float = 0.0,
                 l_6_a: float = 0.0):
        """Initialise Actuator position, velocity and acceleration"""
        self.d_1 = d_1          # lift in mm
        self.theta_1 = theta_1  # swing in degrees
        self.theta_2 = theta_2  # elbow rotation in degrees
        self.theta_3 = theta_3  # wrist rotation in degrees
        self.l_6 = l_6          # jaw opening in mm

        self.d_1_v = d_1_v
        self.theta_1_v = theta_1_v
        self.theta_2_v = theta_2_v
        self.theta_3_v = theta_3_v
        self.l_6_v = l_6_v

        self.d_1_a = d_1_a
        self.theta_1_a = theta_1_a
        self.theta_2_a = theta_2_a
        self.theta_3_a = theta_3_a
        self.l_6_a = l_6_a

    def get_states(self) -> Tuple[float, float, float, float, float]:
        return self.d_1, self.theta_1, self.theta_2, self.theta_3, self.l_6

    def reset_vel_and_acc(self):
        self.d_1_v, self.theta_1_v, self.theta_2_v, self.theta_3_v, self.l_6_v = 0.0, 0.0, 0.0, 0.0, 0.0
        self.d_1_a, self.theta_1_a, self.theta_2_a, self.theta_3_a, self.l_6_a = 0.0, 0.0, 0.0, 0.0, 0.0

    def __str__(self) -> str:
        return (f"ActuatorStates("
                f"Position: d_1={self.d_1}, theta_1={self.theta_1}, theta_2={self.theta_2}, theta_3={self.theta_3}, l_6={self.l_6}; "
                f"Velocity: d_1_v={self.d_1_v}, theta_1_v={self.theta_1_v}, theta_2_v={self.theta_2_v}, theta_3_v={self.theta_3_v}, l_6_v={self.l_6_v}; "
                f"Acceleration: d_1_a={self.d_1_a}, theta_1_a={self.theta_1_a}, theta_2_a={self.theta_2_a}, theta_3_a={self.theta_3_a}, l_6_a={self.l_6_a})")
