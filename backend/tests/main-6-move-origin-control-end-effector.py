import numpy as np

from backend.app.services.ControlSimulator import ControlSimulator
from backend.app.models.RobotCrane import RobotCrane
from backend.app.services.tools.AnimationBuilder import create_control_animation

if __name__ == '__main__':
    """Test control loop with moving origin"""
    robot = RobotCrane()
    robot.set_new_origin((0.4, 0.4, 0.4, np.deg2rad(0)))

    sim = ControlSimulator(robot)
    time_list = np.linspace(0, sim.duration, int(np.ceil(sim.duration / 0.03)))

    org_time_series = []

    for t in time_list:
        sim.trajectory_next_step_real_time(t)
        org_time_series.append(sim.origin_next_step_real_time(t))

    sim.plot_metrics(time_list)

    create_control_animation(sim.act_states_list, org_time_series, robot)
