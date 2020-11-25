import AircraftDynamics
import numpy as np
import matplotlib.pyplot as plt

V = 100
gamma = 0.0
t_min = 0
t_max = 100
step = 0.01
de_time = 0

initial_conditions = {"Velocity" : V, "Flight Path" : gamma, "Start Time" : t_min, "End Time" : t_max,
		 "Time Step" : step, "Time of Change" : de_time}

class Simulation():
    def __init__(self,initial_conditions):
        self.conditions = initial_conditions
        self.steps = int((self.conditions.get("End Time") - self.conditions.get("Start Time")/self.conditions.get("Time Step")))
        self.aircraft = AircraftDynamics.Plane(self.conditions.get("Time Step"))
        self.aircraft.V = self.conditions.get("Velocity")
        self.aircraft.gamma = self.conditions.get("Flight Path")
        self.t_ret = np.array([0])
    def set_initial_trim(self):
        self.aircraft.set_initials()
    def cycle(self):
        for i in range(self.steps):
            self.t_ret = np.append(self.t_ret,i)
            self.aircraft.dynamic_derivatives()
            self.aircraft.update()
            if self.t_ret[i] > 100:
                self.aircraft.del_mod = 1.1
            if self.aircraft.z_e < -2000:
                print("Time to reach 2000 {}".format(self.t_ret[i]))
                break
        fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
        ax1.set(ylabel='alpha')
        ax1.plot(self.t_ret,self.aircraft.alpha_ret,'r--')
        ax2.set(ylabel='gamma')
        ax2.plot(self.t_ret,self.aircraft.gamma_ret,'b--')
        ax3.set(ylabel='theta')
        ax3.plot(self.t_ret,self.aircraft.theta_ret,'g--')
        fig2, (ax4,ax5) = plt.subplots(2, sharex=True)
        ax4.set(ylabel='ub')
        ax4.plot(self.t_ret,self.aircraft.ub_ret,'y--')
        ax5.set(ylabel='wb')
        ax5.plot(self.t_ret,self.aircraft.wb_ret,'c--')
        plt.show()

sim = Simulation(initial_conditions)
sim.set_initial_trim()
sim.cycle()