import AircraftDynamics
import numpy as np
import matplotlib.pyplot as plt

V = 100
gamma = 0.0
t_min = 0
t_max = 400
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
        self.aircraft.gamma_0 = self.conditions.get("Flight Path")
        self.t_ret = np.array([0])
    def set_initial_trim(self):
        self.aircraft.set_initials()
    def cycle(self):
        for i in range(self.steps):
            self.t_ret = np.append(self.t_ret,i * self.conditions.get("Time Step"))
            self.aircraft.dynamic_derivatives()
            self.aircraft.update()
            if i is 100:
                self.aircraft.del_mod = 1.1
        plt.plot(self.t_ret,self.aircraft.ub_ret,'r--')
        plt.plot(self.t_ret,self.aircraft.wb_ret,'bx')
        plt.plot(self.t_ret,self.aircraft.theta_ret,'go')
        plt.show()

sim = Simulation(initial_conditions)
sim.set_initial_trim()
sim.cycle()