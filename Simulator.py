import numpy as np
import matplotlib.pyplot as plt
import Aircraft
import math
V = 120
gamma = 0.08
t_min = 0
t_max = 300
step = 0.01
de_time = 0
h1 = -1000
X_e = 0
sim_conditions = {"Start Time" : t_min, "End Time" : t_max,
		 "Time Step" : step, "Time of Change" : de_time}
aircraft_conditions = {"Velocity" : V, "Flight Path" : gamma, "Altitude" : h1, "Time Step" : step, "X" : X_e}

class Simulator():
    def __init__(self,sim_conditions):
        self.plane = Aircraft.Aircraft(aircraft_conditions)
        self.steps = math.ceil((sim_conditions.get("End Time") - sim_conditions.get("Start Time"))/sim_conditions.get("Time Step"))
        self.t_ret = np.array([])
        self.gamma_ret = np.array([])
        self.alpha_ret = np.array([])
        self.ub_ret = np.array([])
        self.wb_ret  = np.array([])
        self.theta_ret = np.array([])
        self.delta_ret = np.array([])
    def set_initials(self):
        self.plane.set_initials()
        print("Initial conditions: ", self.plane.fetch_state())
    def cycles(self):
        for i in range(self.steps):
            print(i)
            self.plane.get_derivatives()
            self.plane.update_state()
            state = self.plane.fetch_state()
            self.t_ret = np.append(self.t_ret,i * step)
            self.gamma_ret = np.append(self.gamma_ret,math.degrees(state[9]))
            self.alpha_ret = np.append(self.alpha_ret,math.degrees(state[0]))
            self.ub_ret = np.append(self.ub_ret,state[2])
            self.wb_ret = np.append(self.wb_ret,state[3])
            self.delta_ret = np.append(self.delta_ret,self.plane.delta_el)
            if i is 10:
                print("ELEVATOR CHANGE--------")
                self.plane.delta_el = self.plane.delta_el * 1.1
        fig, (ax1,ax2,ax3) = plt.subplots(3, sharex=True)
        ax1.set(ylabel='alpha')
        ax1.plot(self.t_ret,self.alpha_ret,'r--')
        ax2.set(ylabel='gamma')
        ax2.plot(self.t_ret,self.gamma_ret,'b--')
        ax3.set(ylabel='delta')
        ax3.plot(self.t_ret,self.delta_ret,'g--')
        fig2, (ax4,ax5) = plt.subplots(2, sharex=True)
        ax4.set(ylabel='ub')
        ax4.plot(self.t_ret,self.ub_ret,'y--')
        ax5.set(ylabel='wb')
        ax5.plot(self.t_ret,self.wb_ret,'c--')
        plt.show()


sim = Simulator(sim_conditions)
sim.set_initials()
sim.cycles()